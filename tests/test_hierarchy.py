import json
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import PropertyMock, patch

from hypothesis import given
from hypothesis.strategies import characters, one_of, lists, text

from rbackup.struct.hierarchy import Hierarchy

# ========== Constants ==========
TESTING_PACKAGE = "rbackup.struct"
TESTING_MODULE = f"{TESTING_PACKAGE}.hierarchy"


# ========== Tests ==========
class TestHierarchyPaths(unittest.TestCase):
    @given(one_of(text(), characters()))
    def test_returns_correct_path(self, p):
        self.assertEqual(Path(p), Hierarchy(p).path)

    def test_raises_notimplemented_error(self):
        h = Hierarchy("backup")
        with self.assertRaises(NotImplementedError):
            h.gen_metadata()


class TestHierarchyMetadata(unittest.TestCase):
    def setUp(self):
        self.patched_json = patch(f"{TESTING_MODULE}.json")
        self.patched_path = patch.object(
            Hierarchy, "metadata_path", new_callable=PropertyMock, spec_set=Path
        )

        self.mocked_path = self.patched_path.start()
        self.mocked_json = self.patched_json.start()

    @unittest.skip("Figure out how to mock file objects")
    @given(text())
    def test_write_metadata(self, data):
        file_obj = StringIO()
        self.mocked_path.return_value.open.return_value = file_obj

        self.mocked_json.load.return_value = file_obj.getvalue()

        h = Hierarchy("backup")
        h.write_metadata(data)
        read_data = h.read_metadata()

        self.assertEqual(data, read_data)

    def tearDown(self):
        self.patched_json.stop()
        self.patched_path.stop()
