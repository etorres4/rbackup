"""
.. author:: Eric Torres

Unit tests for the Snapshot class.
"""
import doctest
import unittest

from pathlib import Path
from rbackup.hierarchy.snapshot import Snapshot

# ========== Constants ==========
TESTING_MODULE = "rbackup.hierarchy.snapshot"


# ========== Functions ==========
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(TESTING_MODULE))
    return tests
