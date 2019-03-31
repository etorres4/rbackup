"""
.. author:: Eric Torres
:synopsis: Unit tests for the PackageManager module.
"""
import doctest
import subprocess
import unittest

from hypothesis import given, note
from hypothesis.strategies import (
    booleans,
    dictionaries,
    integers,
    iterables,
    lists,
    one_of,
    none,
    text,
)
from pathlib import Path
from rbackup.package_managers.packagemanager import PackageManager
from unittest.mock import patch

# ========== Constants ==========
TESTING_MODULE = "rbackup.package_managers.packagemanager"


# ========== Functions ==========
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(TESTING_MODULE))
    return tests


# ========== Test Cases ==========
class TestCreatePackageManager(unittest.TestCase):
    def setUp(self):
        self.patched_path = patch(f"{TESTING_MODULE}.Path", autospec=Path)
        self.patched_subprocess = patch(f"{TESTING_MODULE}.subprocess.run")
        self.patched_tarfile = patch(f"{TESTING_MODULE}.tarfile.open")
        self.patched_tempfile = patch(f"{TESTING_MODULE}.NamedTemporaryFile")

        self.mocked_path = self.patched_path.start()
        self.mocked_run = self.patched_subprocess.start()
        self.mocked_tarfile = self.patched_tarfile.start()
        self.mocked_tempfile = self.patched_tempfile.start()

        self.cachedir = "/var/cache/pacman/"
        self.db_path = "/var/lib/pacman"
        self.pkglist_cmd = ["pacman", "-Qqe"]
        self.p = PackageManager(self.cachedir, self.db_path, self.pkglist_cmd)

    @given(one_of(text(min_size=1), iterables(text(min_size=1), min_size=1)))
    def test_create_with_valid_values(self, l):
        PackageManager("nothing", "nothing", l)

    @given(one_of(none(), booleans(), integers(), dictionaries(text(), text())))
    def test_incorrect_cmd_type(self, cmd):
        with self.assertRaises(TypeError):
            PackageManager("nothing", "nothing", cmd)

    def test_empty_cmd(self):
        with self.assertRaises(ValueError):
            PackageManager("nothing", "nothing", [])
            PackageManager("nothing", "nothing", set())
            PackageManager("nothing", "nothing", '')

    @given(iterables(one_of(none(), booleans(), integers()), min_size=1))
    def test_wrong_iterable_element_type(self, cmd):
        with self.assertRaises(TypeError):
            PackageManager("nothing", "nothing", cmd)

    def test_empty_str_in_iterable(self):
        with self.assertRaises(ValueError):
            PackageManager("nothing", "nothing", [''])
            PackageManager("nothing", "nothing", ['pacman', ''])

    def tearDown(self):
        self.patched_path.stop()
        self.patched_subprocess.stop()
        self.patched_tarfile.stop()
        self.patched_tempfile.stop()


class TestPackageManagerMethods(unittest.TestCase):
    def setUp(self):
        self.patched_path = patch(f"{TESTING_MODULE}.Path", autospec=Path)
        self.patched_subprocess = patch(f"{TESTING_MODULE}.subprocess.run")
        self.patched_tarfile = patch(f"{TESTING_MODULE}.tarfile.open")
        self.patched_tempfile = patch(f"{TESTING_MODULE}.NamedTemporaryFile")

        self.mocked_path = self.patched_path.start()
        self.mocked_run = self.patched_subprocess.start()
        self.mocked_tarfile = self.patched_tarfile.start()
        self.mocked_tempfile = self.patched_tempfile.start()

        self.cachedir = "/var/cache/pacman/"
        self.db_path = "/var/lib/pacman"
        self.pkglist_cmd = ["pacman", "-Qqe"]
        self.p = PackageManager(self.cachedir, self.db_path, self.pkglist_cmd)

    def test_pkglist(self):
        self.mocked_run.return_value.stdout = "packages"
        self.mocked_tempfile.return_value.name = "tempfile"

        pkglist = self.p._gen_pkglist()

        self.mocked_tempfile.return_value.__enter__.return_value.write.assert_called_with(
            "packages"
        )
        self.assertIsInstance(pkglist, Path)

    def test_pkglist_subprocess_error(self):
        self.mocked_run.side_effect = subprocess.CalledProcessError(1, self.pkglist_cmd)

        self.p._gen_pkglist()
        self.mocked_tempfile.assert_not_called()

    def test_db_archive(self):
        p = Path("tmpfile")
        self.mocked_path.return_value = p

        archive = self.p.gen_db_archive()

        self.assertIsInstance(archive, Path)
        self.mocked_tempfile.assert_called_with(delete=False, suffix=".tar")
        self.mocked_tarfile.assert_called_with(name=p, mode="w")

    def test_db_archive_compress_mode(self):
        p = Path("tmpfile")
        compress = "xz"
        self.mocked_path.return_value = p

        archive = self.p.gen_db_archive(compress)

        self.assertIsInstance(archive, Path)
        self.mocked_tempfile.assert_called_with(delete=False, suffix=".tar.xz")
        self.mocked_tarfile.assert_called_with(name=p, mode="w:xz")

    @given(from_regex(r"(?!gz|bz2|lzma|xz)"))
    def test_db_archive_invalid_compress_mode(self, invalid_mode):
        with self.assertRaises(ValueError):
            self.p.gen_db_archive(invalid_mode)

    def tearDown(self):
        self.patched_path.stop()
        self.patched_subprocess.stop()
        self.patched_tarfile.stop()
        self.patched_tempfile.stop()
