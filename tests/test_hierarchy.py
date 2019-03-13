import rbackup.hierarchy as hierarchy
import unittest

from unittest.mock import MagicMock, patch

class TestHierarchy(unittest.TestCase):
    def setUp(self):
        self.patched_os_path = patch('rbackup.hierarchy.os.path')
        self.mocked_os_path = self.patched_os_path.start()

        self.mocked_os_path.isdir.return_value = True

        self.hier = hierarchy.Hierarchy('/mnt')

    @patch("rbackup.hierarchy.os.path.isdir")
    def test_non_dir(self, patched_false_isdir):
        patched_false_isdir.return_value = False

        with self.assertRaises(ValueError):
            h = hierarchy.Hierarchy('NotADir')

    def test_base_path(self):
        self.assertEqual(self.hier.base_dir, "/mnt")

    def test_prev_snapshot(self):
        raise NotImplementedError

    def test_prev_snapshot_link(self):
        raise NotImplementedError

    def test_curr_snapshot(self):
        raise NotImplementedError

    def test_boot_dir(self):
        raise NotImplementedError

    def test_etc_dir(self):
        raise NotImplementedError

    def test_home_dir(self):
        raise NotImplementedError

    def test_root_home_dir(self):
        raise NotImplementedError

    def tearDown(self):
        self.patched_os_path.stop()
