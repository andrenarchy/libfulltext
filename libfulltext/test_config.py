# copyright © 2018 the libfulltext authors (see AUTHORS.md and LICENSE)
"""Unit tests for config parser"""

import io
import os
from unittest import TestCase, skip
from . import config


class ConfigTestParseFile(TestCase):
    """Tests the config.parse_file function"""

    def test_empty(self):
        """Parsing an empty configuration file should return an empty dict"""
        ret = config.parse_file(io.StringIO(""))
        self.assertDictEqual(ret, {})

    def test_invalid_top_level(self):
        """If the top level data structure is not a dict, an error should result"""
        cfg = "[1, 2, 3]"
        with self.assertRaises(config.ConfigurationError) as ctx:
            config.parse_file(io.StringIO(cfg))
        self.assertIn("Expected top-level datastructure to be a dictionary",
                      str(ctx.exception))

    def test_unknown_entry(self):
        """Test if an unknown entry throws an appropriate exception"""
        cfg = "unknown_entry: 42"
        with self.assertRaises(config.ConfigurationError) as ctx:
            config.parse_file(io.StringIO(cfg))
        self.assertIn("Unknown configuration entry 'unknown_entry'",
                      str(ctx.exception))

    def test_working_1(self):
        """Test one example of a working configuration"""
        cfg = """
            storage_fulltext: /tmp/test
            publishers_elsevier_apikey: "01234567890123456789012345678901"
        """
        expected = {
            "storage_fulltext": "/tmp/test",
            "publishers_elsevier_apikey": "01234567890123456789012345678901"
        }

        cfg = io.StringIO(cfg)
        self.assertDictEqual(config.parse_file(cfg), expected)

    @skip("Currently the required functionality for this is not available.")
    def test_working_2(self):
        """Test a second example of a working configuration"""
        cfg = """
            storage_fulltext: testdir
        """
        expected = {
            "storage_fulltext": os.path.abspath("testdir"),
        }

        cfg = io.StringIO(cfg)
        self.assertDictEqual(config.parse_file(cfg), expected)
