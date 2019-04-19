"""
.. moduleauthor:: Eric Torres

Tests for the rbackup.struct.hierarchy module.
"""
import shutil
import unittest
from pathlib import Path
from unittest.mock import DEFAULT, patch

from hypothesis import given
from hypothesis.strategies import from_regex

from rbackup.struct.hierarchy import Hierarchy

# ========== Constants ==========
TESTING_PACKAGE = "rbackup.struct"
TESTING_MODULE = f"{TESTING_PACKAGE}.hierarchy"


# ========== Tests ==========
class TestHierarchyPaths(unittest.TestCase):
    def setUp(self):
        self.patched_path = patch.multiple(
            Path, exists=DEFAULT, mkdir=DEFAULT, symlink_to=DEFAULT, touch=DEFAULT
        )

        self.mocked_path = self.patched_path.start()

    def test_retrieves_correct_metadata_filename(self):
        self.assertEqual(Hierarchy("/tmp/backup").metadata_path.name, ".metadata")

    @given(from_regex(r"[\w/._-]+", fullmatch=True))
    def test_returns_absolute_path(self, dest):
        try:
            self.assertTrue(Hierarchy(dest).path.is_absolute())
        except PermissionError:
            pass

    def test_raises_notimplemented_error(self):
        h = Hierarchy("/tmp/backup")
        with self.assertRaises(NotImplementedError):
            h._gen_metadata()

    def tearDown(self):
        patch.stopall()


class TestHierarchyMetadata(unittest.TestCase):
    """Only meant to check that data written is the same data that is read."""

    def test_write_metadata(self):
        data = ["test", "data"]
        h = Hierarchy("/tmp/backup")
        h.metadata_path.touch()
        h.write_metadata(data)

        self.assertEqual(data, h.read_metadata())

        shutil.rmtree(h)


class TestHierarchyCleanup(unittest.TestCase):
    """Test that hierarchy cleanup works properly.

    Test cases
    ----------
    * Function stops if system is not symlink attack-resistant
    * If symlink attack-resistant, then only delete metadata when all others false
    * Function only deletes snapshots when told to
    * Function only deletes repository directory when told to
    """

    def setUp(self):
        self.patched_path = patch.multiple(
            Path,
            exists=DEFAULT,
            mkdir=DEFAULT,
            symlink_to=DEFAULT,
            touch=DEFAULT,
            unlink=DEFAULT,
        )
        self.patched_metadata = patch.multiple(
            Hierarchy, read_metadata=DEFAULT, write_metadata=DEFAULT
        )
        self.patched_shutil = patch.multiple(f"{TESTING_MODULE}.shutil", rmtree=DEFAULT)

        self.mocked_path = self.patched_path.start()
        self.mocked_metadata = self.patched_metadata.start()
        self.mocked_shutil = self.patched_shutil.start()

        self.mocked_shutil["rmtree"].avoids_symlink_attacks = True

    def test_stops_on_non_symlink_resistant(self):
        self.mocked_shutil["rmtree"].avoids_symlink_attacks = False
        h = Hierarchy("/tmp/backup")

        h.cleanup(remove_snapshots=True)

        self.mocked_shutil["rmtree"].assert_not_called()

    def tearDown(self):
        patch.stopall()
