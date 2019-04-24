"""
.. moduleauthor:: Eric Torres

Tests for the rbackup.config module.
"""
import os
import unittest

import rbackup.system as system

# ========== Constants ==========
TESTING_PACKAGE = "rbackup"
TESTING_MODULE = f"{TESTING_PACKAGE}.system"


# ========== Tests ==========
class TestUmask(unittest.TestCase):
    @staticmethod
    def get_current_umask():
        """Obtain process umask, and then change it back for testing."""
        orig_umask = os.umask(0)
        os.umask(orig_umask)

        return orig_umask

    def setUp(self):
        self.test_umask = 0o0027
        self.orig_umask = self.get_current_umask()

    def test_original_umask_remains(self):
        # noinspection PyBroadException
        try:
            with system.change_umask(self.test_umask):
                self.assertEqual(self.get_current_umask(), self.test_umask)

                raise BaseException
        except:
            pass

        self.assertEqual(self.get_current_umask(), self.orig_umask)

    def tearDown(self):
        os.umask(self.orig_umask)
