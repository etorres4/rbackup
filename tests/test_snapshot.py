"""
.. author:: Eric Torres

Unit tests for the Snapshot class.
"""
import doctest
import unittest

from pathlib import Path
from rbackup.hierarchy.snapshot import Snapshot

# ========== Constants ==========
TESTING_MODULE = "rbackup.hierarchy.repository"


# ========== Functions ==========
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(TESTING_MODULE))
    return tests


# ========== Test Cases ==========
class TestSnapshot(unittest.TestCase):
    def setUp(self):
        self.snapshot_fullpath = Path("backup/data/snapshot-new")
        self.test_snapshot = Snapshot(self.snapshot_fullpath)

    def test_fullpath(self):
        self.assertEqual(self.test_snapshot.path, self.snapshot_fullpath)

    def test_name(self):
        self.assertEqual(self.test_snapshot.name, "snapshot-new")

    def test_boot_dir(self):
        self.assertEqual(
            self.test_snapshot.boot_dir, self.snapshot_fullpath / "boot"
        )

    def test_etc_dir(self):
        self.assertEqual(
            self.test_snapshot.etc_dir, self.snapshot_fullpath / "etc"
        )

    def test_home_dir(self):
        self.assertEqual(
            self.test_snapshot.home_dir, self.snapshot_fullpath / "home"
        )

    def test_root_home_dir(self):
        self.assertEqual(
            self.test_snapshot.root_home_dir, self.snapshot_fullpath / "root"
        )
