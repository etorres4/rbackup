import doctest
import unittest

from rbackup.hierarchy.repository import Repository
from rbackup.hierarchy.snapshot import Snapshot
from unittest.mock import patch

# ========== Constants  ==========
TESTING_MODULE = "rbackup.hierarchy.repository"
OS_PATH = f"{TESTING_MODULE}.os.path"
OS_PATH_ISDIR = f"{OS_PATH}.isdir"
GLOB_GLOB = f"{TESTING_MODULE}.glob.glob"


# ========== Functions ==========
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(TESTING_MODULE))
    return tests


# ========== Integration Tests ==========
class TestRepository(unittest.TestCase):
    def setUp(self):
        self.patched_isdir = patch(OS_PATH_ISDIR)
        self.mocked_isdir = self.patched_isdir.start()

        self.mocked_isdir.return_value = True

        self.patched_glob = patch(GLOB_GLOB)
        self.mocked_glob = self.patched_glob.start()

        self.snapshots = [
            "backup/data/snapshot-first",
            "backup/data/snapshot-second",
            "backup/data/snapshot-third",
        ]

        self.mocked_glob.return_value = self.snapshots

        self.repo_basepath = "backup"

        self.repo = Repository(self.repo_basepath)

    def test_snapshots(self):
        found_snapshots = [s.path for s in self.repo.snapshots]
        self.assertListEqual(found_snapshots, self.snapshots)

    def test_curr_snapshot_pre_create(self):
        snapshot_name = "third"
        snapshot_path = f"backup/data/snapshot-{snapshot_name}"

        self.assertEqual(self.repo.curr_snapshot.path, snapshot_path)
        self.assertIsInstance(self.repo.curr_snapshot, Snapshot)

    def test_curr_snapshot_post_create(self):
        snapshot_name = "new"
        snapshot_path = f"backup/data/snapshot-{snapshot_name}"

        self.repo.create_snapshot(snapshot_name)
        self.assertEqual(self.repo.curr_snapshot.path, snapshot_path)
        self.assertIsInstance(self.repo.curr_snapshot, Snapshot)

    def tearDown(self):
        self.patched_isdir.stop()
        self.patched_glob.stop()
