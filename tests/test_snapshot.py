"""
.. author:: Eric Torres

Unit tests for the Snapshot class.
"""
import doctest
import unittest

from rbackup.struct.snapshot import Snapshot

# ========== Constants ==========
TESTING_MODULE = "rbackup.struct.snapshot"


# ========== Functions ==========
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(TESTING_MODULE))
    return tests


# ========== Unit Tests ==========
