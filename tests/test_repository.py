import doctest
import unittest

from pathlib import PosixPath
from rbackup.hierarchy.repository import Repository
from rbackup.hierarchy.snapshot import Snapshot
from unittest.mock import patch, PropertyMock

# ========== Constants  ==========
TESTING_MODULE = "rbackup.hierarchy.repository"


# ========== Functions ==========
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(TESTING_MODULE))
    return tests


# ========== Integration Tests ==========
class TestPopulatedRepository(unittest.TestCase):
    def setUp(self):
        self.snapshots = [
            Snapshot("backup/data/snapshot-first"),
            Snapshot("backup/data/snapshot-second"),
            Snapshot("backup/data/snapshot-third"),
        ]

        self.patched_snapshots = patch(
            f"{TESTING_MODULE}.Repository.snapshots", new_callable=PropertyMock
        )
        self.mocked_snapshots = self.patched_snapshots.start()
        self.mocked_snapshots.return_value = self.snapshots

        self.repo_basepath = "backup"
        self.repo = Repository(self.repo_basepath)

    def test_snapshots(self):
        found_snapshots = [s for s in self.repo.snapshots]
        self.assertListEqual(found_snapshots, self.snapshots)

    def test_curr_snapshot_pre_create(self):
        snapshot_name = "third"
        last_snapshot = Snapshot(f"backup/data/snapshot-{snapshot_name}")

        self.assertEqual(self.repo.curr_snapshot.path, last_snapshot.path)
        self.assertIsInstance(self.repo.curr_snapshot, Snapshot)

    def test_curr_snapshot_post_create(self):
        snapshot_name = "new"
        snapshot_path = PosixPath(f"backup/data/snapshot-{snapshot_name}")

        self.repo.create_snapshot(snapshot_name)
        self.assertEqual(self.repo.curr_snapshot.path, snapshot_path)
        self.assertIsInstance(self.repo.curr_snapshot, Snapshot)

    def tearDown(self):
        self.patched_snapshots.stop()


class TestEmptyRepository(unittest.TestCase):
    def setUp(self):
        self.patched_snapshots = patch(
            f"{TESTING_MODULE}.Repository.snapshots", new_callable=PropertyMock
        )
        self.mocked_snapshots = self.patched_snapshots.start()
        self.mocked_snapshots.return_value = []

        self.repo_basepath = "backup"
        self.repo = Repository(self.repo_basepath)

    def test_curr_snapshot_pre_create(self):
        self.assertIsNone(self.repo.curr_snapshot)

    def test_curr_snapshot_post_create(self):
        snapshot_name = "new"
        new_snapshot = Snapshot(f"backup/data/snapshot-{snapshot_name}")

        self.repo.create_snapshot(snapshot_name)
        self.assertEqual(self.repo.curr_snapshot.path, new_snapshot.path)
        self.assertIsInstance(self.repo.curr_snapshot, Snapshot)

    def tearDown(self):
        self.patched_snapshots.stop()
