"""
.. moduleauthor:: Eric Torres

Tests for the rbackup.struct.hierarchy module.
"""
import unittest
from unittest.mock import PropertyMock, mock_open, patch

from hypothesis import given
from hypothesis.strategies import from_regex, text

from rbackup.struct.hierarchy import Hierarchy

# ========== Constants ==========
TESTING_PACKAGE = "rbackup.struct"
TESTING_MODULE = f"{TESTING_PACKAGE}.hierarchy"


# ========== Tests ==========
class TestHierarchyPaths(unittest.TestCase):
    def test_retrieves_correct_metadata_filename(self):
        self.assertEqual(Hierarchy("backup").metadata_path.name, ".metadata")

    @given(from_regex(r"[\w/._-]+", fullmatch=True))
    def test_returns_absolute_path(self, dest):
        self.assertTrue(Hierarchy(dest).path.is_absolute())

    def test_raises_notimplemented_error(self):
        h = Hierarchy("backup")
        with self.assertRaises(NotImplementedError):
            h.gen_metadata()


class TestHierarchyMetadata(unittest.TestCase):
    def setUp(self):
        self.patched_json = patch(f"{TESTING_MODULE}.json")
        self.patched_path = patch.object(
            Hierarchy, "metadata_path", new_callable=PropertyMock, create=True
        )

        self.mocked_path = self.patched_path.start()
        self.mocked_json = self.patched_json.start()

        self.mocked_path.return_value.open = mock_open

    @unittest.skip("Figure out how to mock file objects")
    @given(text())
    def test_write_metadata(self, data):
        h = Hierarchy("backup")
        h.write_metadata(data)
        read_data = h.read_metadata()

        self.assertEqual(data, read_data)

    def tearDown(self):
        self.patched_json.stop()
        self.patched_path.stop()
