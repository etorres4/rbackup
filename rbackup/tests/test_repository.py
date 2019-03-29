# import doctest
import unittest

from hypothesis import given
from hypothesis.strategies import builds, lists, text
from pathlib import Path
from rbackup.hierarchy.repository import Repository
from rbackup.hierarchy.snapshot import Snapshot
from unittest.mock import PropertyMock, patch

# ========== Constants  ==========
TESTING_PACKAGE = "rbackup.hierarchy"
REPO_MODULE = f"{TESTING_PACKAGE}.repository"
SS_MODULE = f"{TESTING_PACKAGE}.snapshot"


# ========== Functions ==========
# @unittest.skip("Repositories create files, this should be mocked out")
# def load_tests(loader, tests, ignore):
#    tests.addTests(doctest.DocTestSuite(REPO_MODULE))
#    return tests


# ========== Integration Tests ==========
class TestRepositoryPreCreate(unittest.TestCase):
    """Test properties of the Repository before running create_snapshot()."""

    def setUp(self):
        self.patched_path = patch.object(
            Repository, "metadata_path", new_callable=PropertyMock
        )
        self.patched_snapshot = patch(
            f"{TESTING_PACKAGE}.repository.Snapshot", spec_set=Snapshot
        )
        self.patched_pickle = patch(f"{TESTING_PACKAGE}.repository.pickle")

        self.mocked_path = self.patched_path.start()
        self.mocked_snapshot = self.patched_snapshot.start()
        self.mocked_pickle = self.patched_pickle.start()

    @given(lists(builds(Snapshot, text()), unique=True))
    def test_empty(self, l):
        self.mocked_pickle.load.return_value = {
            "snapshots": l.copy(),
            "current_snapshot": l[-1] if l else None,
        }
        repo = Repository("backup")

        if l == []:
            self.assertTrue(repo.empty)
        else:
            self.assertFalse(repo.empty)

    @given(lists(builds(Snapshot, text()), unique=True))
    def test_len(self, l):
        self.mocked_pickle.load.return_value = {
            "snapshots": l.copy(),
            "current_snapshot": l[-1] if l else None,
        }

        repo = Repository("backup")

        self.assertEqual(len(repo.snapshots), len(l))

    @given(lists(builds(Snapshot, text()), unique=True))
    def test_current_snapshot(self, l):
        self.mocked_pickle.load.return_value = {
            "snapshots": l.copy(),
            "current_snapshot": l[-1] if l else None,
        }

        if l == []:
            self.mocked_pickle.load.return_value["current_snapshot"] = None
        else:
            self.mocked_pickle.load.return_value["current_snapshot"] = l[-1]
        repo = Repository("backup")

        if l == []:
            self.assertIsNone(repo.current_snapshot)
        else:
            self.assertIsNotNone(repo.current_snapshot)
            self.assertIsInstance(repo.current_snapshot, Snapshot)

    def tearDown(self):
        self.patched_path.stop()
        self.patched_snapshot.stop()
        self.patched_pickle.stop()


class TestRepositoryPostCreate(unittest.TestCase):
    """Test properties of the Repository before running create_snapshot()."""

    def setUp(self):
        self.patched_path = patch.object(
            Repository, "metadata_path", new_callable=PropertyMock
        )
        self.patched_snapshot = patch(
            f"{TESTING_PACKAGE}.repository.Snapshot", spec_set=Snapshot
        )
        self.patched_pickle = patch(f"{TESTING_PACKAGE}.repository.pickle")

        self.mocked_path = self.patched_path.start()
        self.mocked_snapshot = self.patched_snapshot.start()
        self.mocked_pickle = self.patched_pickle.start()

    @given(lists(builds(Snapshot, text()), unique=True))
    def test_empty(self, l):
        self.mocked_pickle.load.return_value = {
            "snapshots": l.copy(),
            "current_snapshot": l[-1] if l else None,
        }

        if l == []:
            self.mocked_pickle.load.return_value["current_snapshot"] = None
        else:
            self.mocked_pickle.load.return_value["current_snapshot"] = l[-1]
        repo = Repository("backup")

        repo.create_snapshot()

        self.assertFalse(repo.empty)

    @given(lists(builds(Snapshot, text()), unique=True))
    def test_len(self, l):
        self.mocked_pickle.load.return_value = {
            "snapshots": l.copy(),
            "current_snapshot": l[-1] if l else None,
        }
        repo = Repository("backup")

        repo.create_snapshot()

        self.assertEqual(len(repo), len(l) + 1)
        self.assertEqual(len(repo.snapshots), len(l) + 1)

    @given(lists(builds(Snapshot, text()), unique=True))
    def test_current_snapshot(self, l):
        self.mocked_pickle.load.return_value = {
            "snapshots": l.copy(),
            "current_snapshot": l[-1] if l else None,
        }
        repo = Repository("backup")

        new_snapshot = repo.create_snapshot()

        self.assertIs(new_snapshot, repo.current_snapshot)
        self.assertIsInstance(new_snapshot, Snapshot)

    def tearDown(self):
        self.patched_path.stop()
        self.patched_snapshot.stop()
        self.patched_pickle.stop()
