import doctest
import unittest

from hypothesis import given
from hypothesis.strategies import booleans, characters, iterables, one_of, none, text
from pathlib import Path
from rbackup.struct.hierarchy import Hierarchy

# ========== Constants ==========
TESTING_MODULE = "rbackup.struct.struct"


# ========== Functions ==========
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(TESTING_MODULE))
    return tests


# ========== Tests ==========
class TestHierarchyPaths(unittest.TestCase):
    @given(one_of(text(), characters()))
    def test_returns_correct_path(self, p):
        self.assertEqual(Path(p), Hierarchy(p).path)

    @given(one_of(iterables(elements=none()), booleans()))
    def test_raises_value_error(self, p):
        with self.assertRaises(TypeError):
            Hierarchy(p)
