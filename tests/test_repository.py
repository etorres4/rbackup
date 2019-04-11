"""
.. author:: Eric Torres

Tests for the rbackup.struct.repository module.
"""
# TODO test that the snapshot returned is actually in the repository
# TODO test creating snapshots, returned snapshot is an instance of Snapshot, etc.

import unittest
from unittest.mock import PropertyMock, patch

from hypothesis import given
from hypothesis.strategies import characters, lists, text

from rbackup.struct.repository import Repository
from rbackup.struct.snapshot import Snapshot

# ========== Constants  ==========
TESTING_PACKAGE = "rbackup.struct"
REPO_MODULE = f"{TESTING_PACKAGE}.repository"
SS_MODULE = f"{TESTING_PACKAGE}.snapshot"

UNWANTED_SNAPSHOT_CHARS = ["/"]


# ========== Integration Tests ==========
class TestRepositoryPreCreate(unittest.TestCase):
    """Test properties of the Repository before running create_snapshot().

    Mocked Modules/Classes
    ----------------------
    rbackup.struct.repository.Snapshot

    Mocked Attributes
    -----------------
    * Repository.metadata_path
    * Repository.read_metadata
    * Repository.write_metadata
    """

    def setUp(self):
        self.patched_path = patch.object(
            Repository, "metadata_path", new_callable=PropertyMock
        )
        self.patched_r_metadata = patch.object(
            Repository, "read_metadata", spec_set=list
        )
        self.patched_w_metadata = patch.object(
            Repository, "write_metadata", spec_set=list
        )
        self.patched_snapshot = patch(
            f"{TESTING_PACKAGE}.repository.Snapshot", spec_set=Snapshot
        )

        self.mocked_r_metadata = self.patched_r_metadata.start()
        self.mocked_w_metadata = self.patched_w_metadata.start()
        self.mocked_path = self.patched_path.start()
        self.mocked_snapshot = self.patched_snapshot.start()

        self.mocked_path.return_value.exists.return_value = True

    @given(
        lists(
            text(
                alphabet=characters(blacklist_characters=UNWANTED_SNAPSHOT_CHARS),
                min_size=1,
            ),
            unique=True,
        )
    )
    def test_empty(self, snapshots):
        self.mocked_r_metadata.return_value = snapshots.copy()
        repo = Repository("backup")

        if not snapshots:
            self.assertTrue(repo.empty)
        else:
            self.assertFalse(repo.empty)

    @given(
        lists(
            text(
                alphabet=characters(blacklist_characters=UNWANTED_SNAPSHOT_CHARS),
                min_size=1,
            ),
            unique=True,
        )
    )
    def test_len(self, snapshots):
        self.mocked_r_metadata.return_value = snapshots.copy()
        repo = Repository("backup")

        self.assertEqual(len(repo.snapshots), len(snapshots))

    @given(text(min_size=1))
    def test_contains(self, name):
        self.mocked_r_metadata = []
        repo = Repository("backup")

        self.assertFalse(name in repo)

    @given(text())
    def test_valid_name(self, name):
        self.mocked_r_metadata.return_value = []

        if not name or "/" in name:
            self.assertFalse(Repository.is_valid_snapshot_name(name))
        else:
            self.assertTrue(Repository.is_valid_snapshot_name(name))

    def test_snapshots_returns_empty_list(self):
        r = Repository("backup")
        self.assertListEqual(r.snapshots, [])

    def tearDown(self):
        self.patched_path.stop()
        self.patched_r_metadata.stop()
        self.patched_w_metadata.stop()
        self.patched_snapshot.stop()


class TestRepositoryPostCreate(unittest.TestCase):
    """Test properties of the Repository after running create_snapshot().

    Mocked Modules/Classes
    ----------------------
    rbackup.struct.repository.Snapshot

    Mocked Attributes
    -----------------
    * Repository.metadata_path
    * Repository.read_metadata
    * Repository.write_metadata
    """

    def setUp(self):
        self.patched_path = patch.object(
            Repository, "metadata_path", new_callable=PropertyMock
        )
        self.patched_r_metadata = patch.object(
            Repository, "read_metadata", spec_set=list
        )
        self.patched_w_metadata = patch.object(
            Repository, "write_metadata", spec_set=list
        )
        self.patched_snapshot = patch(
            f"{TESTING_PACKAGE}.repository.Snapshot", spec_set=Snapshot
        )

        self.mocked_path = self.patched_path.start()
        self.mocked_r_metadata = self.patched_r_metadata.start()
        self.mocked_w_metadata = self.patched_w_metadata.start()
        self.mocked_snapshot = self.patched_snapshot.start()

    @given(
        lists(
            text(
                alphabet=characters(blacklist_characters=UNWANTED_SNAPSHOT_CHARS),
                min_size=1,
            ),
            unique=True,
        )
    )
    def test_empty(self, snapshots):
        self.mocked_r_metadata.return_value = snapshots.copy()
        repo = Repository("backup")

        repo.create_snapshot()

        self.assertFalse(repo.empty)

    @given(
        lists(
            text(
                alphabet=characters(blacklist_characters=UNWANTED_SNAPSHOT_CHARS),
                min_size=1,
            ),
            unique=True,
        )
    )
    def test_len(self, snapshots):
        self.mocked_r_metadata.return_value = snapshots.copy()
        repo = Repository("backup")

        repo.create_snapshot()

        self.assertEqual(len(repo), len(snapshots) + 1)
        self.assertEqual(len(repo.snapshots), len(snapshots) + 1)

    @given(
        text(
            alphabet=characters(blacklist_characters=UNWANTED_SNAPSHOT_CHARS),
            min_size=1,
        )
    )
    def test_contains(self, name):
        self.mocked_path.return_value.exists.return_value = False
        repo = Repository("backup")

        repo.create_snapshot(name)
        self.assertTrue(name in repo)

    def tearDown(self):
        self.patched_path.stop()
        self.patched_r_metadata.stop()
        self.patched_w_metadata.stop()
        self.patched_snapshot.stop()
