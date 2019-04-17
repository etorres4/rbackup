"""
.. moduleauthor:: Eric Torres

Unit tests for the rbackup.struct.snapshot module.
"""

import unittest
from pathlib import Path
from unittest.mock import DEFAULT, patch

from rbackup.struct.snapshot import Snapshot

# ========== Constants ==========
TESTING_PACKAGE = "rbackup.struct"
TESTING_MODULE = f"{TESTING_PACKAGE}.snapshot"


# ========== Tests ==========
class TestSnapshotProperties(unittest.TestCase):
    def setUp(self):
        self.patched_path = patch.multiple(
            Path, exists=DEFAULT, mkdir=DEFAULT, symlink_to=DEFAULT, touch=DEFAULT
        )
        self.patched_metadata = patch.multiple(
            Snapshot, read_metadata=DEFAULT, write_metadata=DEFAULT
        )

        self.mocked_path = self.patched_path.start()
        self.mocked_metadata = self.patched_metadata.start()

        self.mocked_path["exists"].return_value = False

    def test_ctime_returns_str(self):
        self.assertIsInstance(Snapshot("/tmp/backup/snapshot").ctime, str)

    def tearDown(self):
        self.patched_path.stop()
        self.patched_metadata.stop()
