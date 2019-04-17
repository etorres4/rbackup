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
            h.gen_metadata()

    def tearDown(self):
        self.patched_path.stop()


class TestHierarchyMetadata(unittest.TestCase):
    """Only meant to check that data written is the same data that is read."""

    def test_write_metadata(self):
        data = ["test", "data"]
        h = Hierarchy("/tmp/backup")
        h.metadata_path.touch()
        h.write_metadata(data)

        self.assertEqual(data, h.read_metadata())

        shutil.rmtree(h)
