"""
.. moduleauthor:: Eric Torres
:synopsis: Unit tests for the PackageManager module.
"""
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from hypothesis import given
from hypothesis.strategies import from_regex, iterables, one_of, text

from rbackup.package_managers.packagemanager import PackageManager

# ========== Constants ==========
TESTING_MODULE = "rbackup.package_managers.packagemanager"


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

        pkglist = self.p.gen_pkglist()

        self.mocked_tempfile.return_value.__enter__.return_value.write.assert_called_with(
            "packages"
        )
        self.assertIsInstance(pkglist, Path)

    def test_pkglist_subprocess_error(self):
        self.mocked_run.side_effect = subprocess.CalledProcessError(1, self.pkglist_cmd)

        self.p.gen_pkglist()
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
