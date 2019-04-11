import json
import unittest

from hypothesis import given
from hypothesis.strategies import booleans, characters, iterables, one_of, none, text
from pathlib import Path
from rbackup.struct.hierarchy import Hierarchy

# ========== Constants ==========
TESTING_PACKAGE = "rbackup.struct"
TESTING_MODULE = f"{TESTING_PACKAGE}.hierarchy"


# ========== Tests ==========
class TestHierarchyPaths(unittest.TestCase):
    @given(one_of(text(), characters()))
    def test_returns_correct_path(self, p):
        self.assertEqual(Path(p), Hierarchy(p).path)

    @given(one_of(iterables(elements=none()), booleans()))
    def test_raises_value_error(self, p):
        with self.assertRaises(TypeError):
            Hierarchy(p)
