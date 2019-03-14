import rbackup.hierarchy as hierarchy
import unittest

from unittest.mock import patch

# ========== Constants ==========


# ========== Test Cases ==========
class TestHierarchy(unittest.TestCase):
    @patch("rbackup.hierarchy.os.path.isdir")
    def test_base_path(self, mocked_isdir):
        mocked_isdir.return_value = True

        self.assertEqual(hierarchy.Hierarchy("directory").base_path, "directory")

    @patch("rbackup.hierarchy.os.path.isdir")
    def test_invalid_dir(self, mocked_isdir):
        mocked_isdir.return_value = False

        with self.assertRaises(NotADirectoryError):
            hierarchy.Hierarchy("notadirectory")


class TestRepository(unittest.TestCase):
    def setUp(self):
        self.patched_isdir = patch("rbackup.hierarchy.os.path.isdir")
        self.mocked_isdir = self.patched_isdir.start()

        self.mocked_isdir.return_value = True

        self.patched_datetime = patch("rbackup.hierarchy.datetime")
        self.mocked_datetime = self.patched_datetime.start()

        self.mocked_datetime.datetime.utcnow.return_value.isoformat.return_value = (
            "utcnow"
        )

        self.patched_glob = patch("rbackup.hierarchy.glob.glob")
        self.mocked_glob = self.patched_glob.start()

        self.mocked_glob.return_value = [
            "backup/data/snapshot-first",
            "backup/data/snapshot-second",
            "backup/data/snapshot-last",
        ]

        self.repo = hierarchy.Repository("backup")

    @patch("rbackup.hierarchy.glob.glob")
    def test_first_snapshot(self, mocked_glob):
        mocked_glob.return_value = []

        empty_repo = hierarchy.Repository("backup")

        self.assertIsNone(empty_repo.snapshots)

    @patch("rbackup.hierarchy.os.path.realpath")
    def test_prev_snapshot(self, mocked_realpath):
        mocked_realpath.return_value = "backup/data/snapshot-last"

        self.assertEqual(self.repo.prev_snapshot.path, "backup/data/snapshot-last")

        self.assertIsInstance(self.repo.prev_snapshot, hierarchy.Snapshot)

    def test_curr_snapshot(self):
        self.assertEqual(self.repo.curr_snapshot.path, "backup/data/snapshot-utcnow")

    def tearDown(self):
        self.patched_isdir.stop()
        self.patched_datetime.stop()
        self.patched_glob.stop()


class TestSnapshot(unittest.TestCase):
    def setUp(self):
        self.patched_isdir = patch("rbackup.hierarchy.os.path.isdir")
        self.mocked_isdir = self.patched_isdir.start()

        self.mocked_isdir.return_value = True

        self.patched_datetime = patch("rbackup.hierarchy.datetime")
        self.mocked_datetime = self.patched_datetime.start()

        self.mocked_datetime.datetime.utcnow.return_value.isoformat.return_value = (
            "utcnow"
        )

        self.snapshot = hierarchy.Snapshot("backup/data/snapshot-utcnow")

    def test_name(self):
        self.assertEqual(self.snapshot.name, "snapshot-utcnow")

    def test_boot_dir(self):
        self.assertEqual(self.snapshot.boot_dir, "backup/data/snapshot-utcnow/boot")

    def test_etc_dir(self):
        self.assertEqual(self.snapshot.etc_dir, "backup/data/snapshot-utcnow/etc")

    def test_home_dir(self):
        self.assertEqual(self.snapshot.home_dir, "backup/data/snapshot-utcnow/home")

    def test_root_home_dir(self):
        self.assertEqual(
            self.snapshot.root_home_dir, "backup/data/snapshot-utcnow/root"
        )

    def tearDown(self):
        self.patched_isdir.stop()
        self.patched_datetime.stop()
