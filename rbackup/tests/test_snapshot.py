"""
.. author:: Eric Torres

Unit tests for the Snapshot class.
"""
import doctest
import unittest

from rbackup.hierarchy.snapshot import Snapshot
from unittest.mock import patch

# ========== Constants ==========
TESTING_MODULE = "rbackup.hierarchy.snapshot"


# ========== Functions ==========
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(TESTING_MODULE))
    return tests


# ========= Classes ==========
class TestSnapshot(unittest.TestCase):
    def setUp(self):
        self.patched_path = patch(f"{TESTING_MODULE}.Hierarchy")
        self.mocked_path = self.patched_path.start()

    def tearDown(self):
        self.patched_path.stop()
