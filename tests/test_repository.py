"""
.. moduleauthor:: Eric Torres

Tests for the rbackup.struct.repository module.
"""
import re
import unittest
from pathlib import Path
from unittest.mock import DEFAULT, PropertyMock, patch

from hypothesis import given
from hypothesis.strategies import from_regex, lists, text

from rbackup.struct.repository import Repository
from rbackup.struct.snapshot import Snapshot

# ========== Constants  ==========
TESTING_PACKAGE = "rbackup.struct"
TESTING_MODULE = f"{TESTING_PACKAGE}.repository"
SS_MODULE = f"{TESTING_PACKAGE}.snapshot"

VALID_SNAPSHOT_NAME = r"[\w._@:+-]+[^/]*"


# ========== Integration Tests ==========
class TestRepositoryPreCreate(unittest.TestCase):
    """Test properties of the Repository before running create_snapshot().

    Mocked Modules/Classes
    ----------------------
    rbackup.struct.repository.Snapshot

    Mocked Attributes
    -----------------
    * Repository.read_metadata
    * Repository.write_metadata
    """

    def setUp(self):
        self.patched_path = patch.multiple(
            Path, exists=DEFAULT, mkdir=DEFAULT, symlink_to=DEFAULT, touch=DEFAULT
        )
        self.patched_metadata = patch.multiple(
            Repository, read_metadata=DEFAULT, write_metadata=DEFAULT
        )
        self.patched_snapshot = patch(
            f"{TESTING_PACKAGE}.repository.Snapshot", spec_set=Snapshot
        )

        self.mocked_path = self.patched_path.start()
        self.mocked_metadata = self.patched_metadata.start()
        self.mocked_snapshot = self.patched_snapshot.start()

        self.mocked_path["exists"].return_value = True

    @given(lists(from_regex(VALID_SNAPSHOT_NAME, fullmatch=True), unique=True))
    def test_empty(self, snapshots):
        self.mocked_metadata["read_metadata"].return_value = snapshots.copy()
        repo = Repository("/tmp/backup")

        if not snapshots:
            self.assertTrue(repo.empty)
        else:
            self.assertFalse(repo.empty)

    @given(lists(from_regex(VALID_SNAPSHOT_NAME, fullmatch=True), unique=True))
    def test_dunder_len(self, snapshots):
        self.mocked_metadata["read_metadata"].return_value = snapshots.copy()
        repo = Repository("/tmp/backup")

        self.assertEqual(len(repo.snapshots), len(snapshots))

    @given(text(min_size=1))
    def test_dunder_contains(self, name):
        self.mocked_metadata["read_metadata"].return_value = []
        repo = Repository("/tmp/backup")

        self.assertFalse(name in repo)

    @given(text())
    def test_valid_name(self, name):
        self.mocked_metadata["read_metadata"].return_value = []

        if not re.match(VALID_SNAPSHOT_NAME, name):
            self.assertFalse(Repository.is_valid_snapshot_name(name))
        else:
            self.assertTrue(Repository.is_valid_snapshot_name(name))

    def test_snapshots_returns_empty_list(self):
        repo = Repository("/tmp/backup")
        self.assertListEqual(repo.snapshots, [])

    @given(
        lists(from_regex(VALID_SNAPSHOT_NAME, fullmatch=True), min_size=1, unique=True)
    )
    def snapshots_property_contains_snapshot_objects(self, snapshots):
        self.mocked_metadata["read_metadata"].return_value = snapshots
        repo = Repository("/tmp/backup")

        self.assertTrue(all(isinstance(p, Snapshot) for p in repo))

    def tearDown(self):
        patch.stopall()


class TestRepositoryPostCreate(unittest.TestCase):
    """Test properties of the Repository after running create_snapshot().

    Mocked Modules/Classes
    ----------------------
    rbackup.struct.repository.Snapshot

    Mocked Attributes
    -----------------
    * Repository.read_metadata
    * Repository.write_metadata
    """

    def setUp(self):
        self.patched_path = patch.multiple(
            Path, exists=DEFAULT, mkdir=DEFAULT, symlink_to=DEFAULT, touch=DEFAULT
        )
        self.patched_metadata = patch.multiple(
            Repository, read_metadata=DEFAULT, write_metadata=DEFAULT
        )
        self.patched_snapshot = patch(
            f"{TESTING_PACKAGE}.repository.Snapshot", spec_set=Snapshot
        )

        self.mocked_path = self.patched_path.start()
        self.mocked_metadata = self.patched_metadata.start()
        self.mocked_snapshot = self.patched_snapshot.start()

        self.mocked_path["exists"].return_value = True

    @given(lists(from_regex(VALID_SNAPSHOT_NAME, fullmatch=True), unique=True))
    def test_dunder_len(self, snapshots):
        self.mocked_metadata["read_metadata"].return_value = snapshots.copy()
        repo = Repository("/tmp/backup")

        repo.create_snapshot()

        self.assertEqual(len(repo), len(snapshots) + 1)
        self.assertEqual(len(repo.snapshots), len(snapshots) + 1)

    @given(from_regex(VALID_SNAPSHOT_NAME, fullmatch=True))
    def test_dunder_contains(self, name):
        self.mocked_path["exists"].return_value = False
        repo = Repository("/tmp/backup")

        repo.create_snapshot(name)
        self.assertTrue(name in repo)

    def test_empty(self):
        self.mocked_metadata["read_metadata"].return_value = []
        repo = Repository("/tmp/backup")

        repo.create_snapshot()

        self.assertFalse(repo.empty)

    def test_snapshot_returns_snapshot_object(self):
        self.mocked_metadata["read_metadata"].return_value = []
        repo = Repository("/tmp/backup")

        self.assertIsInstance(repo.create_snapshot(), Snapshot)

    def test_create_duplicate_snapshot(self):
        # Test that if a snapshot is a duplicate, then return that duplicate snapshot
        self.mocked_metadata["read_metadata"].return_value = []
        repo = Repository("/tmp/backup")
        name = "new-snapshot"

        first = repo.create_snapshot(name)
        second = repo.create_snapshot(name)

        self.assertIs(first, second)
        self.assertTrue(name in repo)
        self.assertEqual(len(repo), 1)

    def tearDown(self):
        patch.stopall()


class TestRepositoryCleanup(unittest.TestCase):
    """Test that repository cleanup works properly.

    Test cases
    ----------
    * Function stops if system is not symlink attack-resistant
    * If symlink attack-resistant, then only delete metadata when all others false
    * Function only deletes snapshots when told to
    * Function only deletes repository directory when told to
    """

    def setUp(self):
        self.patched_path = patch.multiple(
            Path,
            exists=DEFAULT,
            mkdir=DEFAULT,
            symlink_to=DEFAULT,
            touch=DEFAULT,
            unlink=DEFAULT,
        )
        self.patched_metadata = patch.multiple(
            Repository, read_metadata=DEFAULT, write_metadata=DEFAULT
        )
        self.patched_snapshot = patch(
            f"{TESTING_PACKAGE}.repository.Snapshot", spec_set=Snapshot
        )
        self.patched_shutil = patch.multiple(f"{TESTING_MODULE}.shutil", rmtree=DEFAULT)

        self.mocked_path = self.patched_path.start()
        self.mocked_metadata = self.patched_metadata.start()
        self.mocked_shutil = self.patched_shutil.start()
        self.mocked_snapshot = self.patched_snapshot.start()

        self.mocked_shutil["rmtree"].avoids_symlink_attacks = True

    def test_stops_on_non_symlink_resistant(self):
        self.mocked_shutil["rmtree"].avoids_symlink_attacks = False
        repo = Repository("/tmp/backup")

        repo.cleanup(remove_snapshots=True)

        self.mocked_path["unlink"].assert_not_called()
        self.mocked_shutil["rmtree"].assert_not_called()

    @patch.object(Repository, "snapshot_symlink", new_callable=PropertyMock)
    @patch.object(Repository, "metadata_path", new_callable=PropertyMock)
    def test_removes_metadata_by_default(
        self, mocked_metadata_path, mocked_snapshot_symlink
    ):
        repo = Repository("/tmp/backup")

        repo.cleanup()

        mocked_metadata_path.return_value.unlink.assert_called_once()
        mocked_snapshot_symlink.return_value.unlink.assert_called_once()

    def test_removes_snapshots(self):
        repo = Repository("/tmp/backup")

        repo.cleanup(remove_snapshots=True)

        self.mocked_shutil["rmtree"].assert_called_once()

    def test_removes_repo_dir(self):
        repo = Repository("/tmp/backup")

        repo.cleanup(remove_repo_dir=True)

        self.mocked_shutil["rmtree"].assert_called_once()

    def tearDown(self):
        patch.stopall()
