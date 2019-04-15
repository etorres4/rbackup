"""
.. moduleauthor:: Eric Torres

Tests for the rbackup.config module.
"""
import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile
from unittest.mock import patch

import rbackup.config as config

# ========== Constants ==========
TESTING_PACKAGE = "rbackup"
TESTING_MODULE = f"{TESTING_PACKAGE}.config"


# ========== Tests ==========
class TestMergeFiles(unittest.TestCase):
    def setUp(self):
        self.patched_path = patch(f"{TESTING_MODULE}.Path", spec_set=Path)
        self.patched_tempfile = patch(
            f"{TESTING_MODULE}.NamedTemporaryFile", spec_set=NamedTemporaryFile
        )

        self.mocked_path = self.patched_path.start()
        self.mocked_tempfile = self.patched_tempfile.start()

    def test_returns_path_object(self):
        self.assertIsInstance(config.merge_files([]), Path)

    def tearDown(self):
        self.patched_path.stop()
        self.patched_tempfile.stop()


class TestParseConfig(unittest.TestCase):
    def setUp(self):
        self.patched_config_file = patch(f"{TESTING_MODULE}.MAIN_CONFIG_FILE", spec_set=Path)
        self.patched_path = patch(f"{TESTING_MODULE}.Path", spec_set=Path)

        self.mocked_config_file = self.patched_config_file.start()
        self.mocked_path = self.patched_path.start()

    def test_raises_file_not_found_error(self):
        self.mocked_config_file.is_file.return_value = False

        with self.assertRaises(FileNotFoundError):
            config.parse_configfile()

    def tearDown(self):
        self.patched_config_file.stop()
        self.patched_path.stop()