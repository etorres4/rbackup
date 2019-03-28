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
@patch.object(Repository, "snapshots", new_callable=PropertyMock)
class TestEmptyRepository(unittest.TestCase):
    """Test a repository that has no snapshots."""

    def setUp(self):
        self.repo_basepath = "backup"
        self.repo = Repository(self.repo_basepath)
        self.new_snapshot_path = self.repo.snapshot_dir / "snapshot-new"
        self.created_snapshot = Snapshot(self.new_snapshot_path)

    def test_len_pre_create(self, repo_snapshots):
        repo_snapshots.return_value = []

        self.assertEqual(len(self.repo), 0)
        self.assertEqual(len(self.repo), len(repo_snapshots.return_value))

    def test_iteration_pre_create(self, repo_snapshots):
        repo_snapshots.return_value = []

        with self.assertRaises(StopIteration):
            self.repo.__next__()

    def test_subscript_pre_create(self, repo_snapshots):
        repo_snapshots.return_value = []

        with self.assertRaises(IndexError):
            self.repo[0]

    def test_curr_snapshot_pre_create(self, repo_snapshots):
        repo_snapshots.return_value = []

        self.assertIsNone(self.repo.curr_snapshot)

    def test_curr_snapshot_post_create(self, repo_snapshots):
        repo_snapshots.return_value = []

        snapshot_name = "new"

        self.repo.create_snapshot(snapshot_name)

        self.assertEqual(self.repo.curr_snapshot.path, self.created_snapshot.path)

    def test_len_post_create(self, repo_snapshots):
        repo_snapshots.return_value = [self.created_snapshot.path]
        self.assertEqual(len(self.repo), len(repo_snapshots.return_value))

    def test_iteration_post_create(self, repo_snapshots):
        repo_snapshots.return_value = [self.created_snapshot]

        result = []
        for snapshot in self.repo:
            result.append(snapshot)

        self.assertListEqual(result, [self.created_snapshot])

    def test_subscript_post_create(self, repo_snapshots):
        repo_snapshots.return_value = [self.created_snapshot]

        self.assertEqual(self.repo[0].path, self.new_snapshot_path)


@patch.object(Repository, "snapshots", new_callable=PropertyMock)
class TestPopulatedRepository(unittest.TestCase):
    """Test a repository that has no snapshots."""

    def setUp(self):
        self.repo_basepath = "backup"
        self.repo = Repository(self.repo_basepath)

        self.new_snapshot_path_1 = self.repo.snapshot_dir / "snapshot-one"
        self.new_snapshot_path_2 = self.repo.snapshot_dir / "snapshot-two"

        self.existing_snapshots = [
            Snapshot(self.new_snapshot_path_1),
            Snapshot(self.new_snapshot_path_2),
        ]

    def test_len_pre_create(self, repo_snapshots):
        repo_snapshots.return_value = self.existing_snapshots
        self.assertEqual(len(self.repo), len(repo_snapshots.return_value))

    def test_iteration_pre_create(self, repo_snapshots):
        repo_snapshots.return_value = self.existing_snapshots

        # Exhaust the iterator first
        for iteration in range(0, len(self.existing_snapshots)):
            self.repo.__next__()

        with self.assertRaises(StopIteration):
            self.repo.__next__()

    def test_subscript_pre_create(self, repo_snapshots):
        repo_snapshots.return_value = self.existing_snapshots

        with self.assertRaises(IndexError):
            self.repo[len(self.repo) + 1]

        with self.assertRaises(IndexError):
            self.repo[-1 * len(self.repo) - 1]

    def test_curr_snapshot_pre_create(self, repo_snapshots):
        repo_snapshots.return_value = self.existing_snapshots

        self.assertListEqual(self.repo.snapshots, self.existing_snapshots)

    def test_curr_snapshot_post_create(self, repo_snapshots):
        """We want to combine all of the tests before the snapshot
        creation into one snapshot so as to not repeat the creation
        of a new snapshot for each test."""
        repo_snapshots.return_value = self.existing_snapshots

        snapshot_name = "new"

        self.repo.create_snapshot(snapshot_name)

        self.new_snapshot_path_3 = self.repo.snapshot_dir / f"snapshot-{snapshot_name}"

        self.assertEqual(self.repo.curr_snapshot.path, self.new_snapshot_path_3)

        # Test that len works correctly
        self.assertEqual(len(self.repo), len(self.existing_snapshots))

        # Test that iteration works correctly
        result = []
        for snapshot in self.repo:
            result.append(snapshot)

        self.assertListEqual(result, self.existing_snapshots)

        repo_snapshots.return_value = self.existing_snapshots

        # Test that subscripts work correctly
        self.assertEqual(self.repo[0].path, self.existing_snapshots[0].path)
        self.assertEqual(self.repo[-1].path, self.existing_snapshots[-1].path)
