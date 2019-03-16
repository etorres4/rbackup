"""
.. author:: Eric Torres

Unit tests for the Snapshot class.
"""
import doctest
import unittest

from rbackup.hierarchy.snapshot import Snapshot
from unittest.mock import patch

# ========== Constants ==========
TESTING_MODULE = "rbackup.hierarchy.repository"

# ========== Functions ==========
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(TESTING_MODULE))
    return tests


# ========== Test Cases ==========
class TestSnapshot(unittest.TestCase):
    def setUp(self):
        self.patched_isdir = patch("rbackup.hierarchy.snapshot.os.path.isdir")
        self.mocked_isdir = self.patched_isdir.start()

        self.mocked_isdir.return_value = True

        self.snapshot_fullpath = "backup/data/snapshot-new"
        self.snapshot_name = "snapshot-new"

        self.snapshot = Snapshot(self.snapshot_fullpath)

    def test_path(self):
        self.assertEqual(self.snapshot.path, self.snapshot_fullpath)

    def test_name(self):
        self.assertEqual(self.snapshot.name, self.snapshot_name)

    def test_boot_dir(self):
        self.assertEqual(self.snapshot.boot_dir, f"{self.snapshot_fullpath}/boot")

    def test_etc_dir(self):
        self.assertEqual(self.snapshot.etc_dir, f"{self.snapshot_fullpath}/etc")

    def test_home_dir(self):
        self.assertEqual(self.snapshot.home_dir, f"{self.snapshot_fullpath}/home")

    def test_root_home_dir(self):
        self.assertEqual(self.snapshot.root_home_dir, f"{self.snapshot_fullpath}/root")

    def tearDown(self):
        self.patched_isdir.stop()
