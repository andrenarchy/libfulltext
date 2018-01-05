# copyright © 2018 the libfulltext authors (see AUTHORS.md and LICENSE)
"""Unit tests for config parser"""

import io
import os
from unittest import TestCase, skip
import yaml
from . import config


class MinimalConfiguration:
    """
    Class which defines properties to quickly generate
    a minimal working configuration for testing.

    This class needs to be adapted whenever new configuration
    entries are added to configdata.yaml, which are marked as required.
    """
    @property
    def minimal_configuration(self):
        """Return the minimal dummy configuration as a dict"""
        return {
            "publishers_elsevier_apikey": "01234567890123456789012345678901",
        }

    @property
    def minimal_configfile(self):
        """Return the minimal dummy configuration as a parsable stream"""
        return io.StringIO(yaml.safe_dump(self.minimal_configuration))

    @property
    def minimal_environment(self):
        """Return the minimal dummy configuration as an OS environment"""
        return {"LIBFULLTEXT_" + key.upper(): value
                for key, value in self.minimal_configuration.items()}


class EnvironmentVariables:
    # pylint: disable=too-few-public-methods
    """Context manager to temporarily manipulate the OS environment variables"""
    def __init__(self, environ):
        self.temp_environ = environ
        self.orig_environ = os.environ

    def __enter__(self):
        os.environ = self.temp_environ

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.environ = self.orig_environ


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


class ConfigTestParseEnvironment(TestCase):
    """Tests the config.parse_environment function"""

    @property
    def base_environment(self):
        """The basic os environment to use for testing"""
        return {
            "PATH": "/bin:/usr/bin",
            "HOME": "/tmp",
            "FULLTEXT_PUBLISHERS_ELSEVIER_APIKEY": "abc"
        }

    def test_empty(self):
        """
        Parsing an environment without any keys for libfulltext should yield empty dict
        """
        with EnvironmentVariables(self.base_environment):
            self.assertDictEqual(config.parse_environment(), {})

    def test_unknown_envvar(self):
        """Test if an unknown environment variables, throws an appropriate exception"""
        env_vars = self.base_environment
        env_vars["LIBFULLTEXT_UNKNOWN_ENTRY"] = "42"
        with self.assertRaises(config.ConfigurationError) as ctx:
            with EnvironmentVariables(env_vars):
                config.parse_environment()
        self.assertIn("Cannot associate environment variable 'LIBFULLTEXT_UNKNOWN_ENTRY'",
                      str(ctx.exception))

    def test_working_1(self):
        """Test one example of a working configuration"""
        env_vars = self.base_environment
        apikey = "01234567890123456789012345678901"
        env_vars["LIBFULLTEXT_PUBLISHERS_ELSEVIER_APIKEY"] = apikey
        env_vars["LIBFULLTEXT_STORAGE_FULLTEXT"] = "/tmp/test"

        expected = {
            "storage_fulltext": "/tmp/test",
            "publishers_elsevier_apikey": apikey
        }
        with EnvironmentVariables(env_vars):
            self.assertDictEqual(config.parse_environment(), expected)

    @skip("Currently the required functionality for this is not available.")
    def test_working_2(self):
        """Test a second example of a working configuration"""
        env_vars = self.base_environment
        env_vars["LIBFULLTEXT_STORAGE_FULLTEXT"] = "testdir"

        expected = {
            "storage_fulltext": os.path.abspath("testdir"),
        }
        with EnvironmentVariables(env_vars):
            self.assertDictEqual(config.parse_environment(), expected)


class ConfigTestNormalise(TestCase, MinimalConfiguration):
    """
    Test the config.normalise function
    """
    def test_complete_config_passes(self):
        """
        Test whethere a complete config passes without problems.
        If this test fails it could indicate that the
        MinimalConfiguration class has not been updated.
        """
        config.normalise(self.minimal_configuration)

    def test_detect_missing_required(self):
        """Test that it is detected if some required values are missing"""
        deleted = "publishers_elsevier_apikey"

        # Take complete configuration and remove a key
        raw = self.minimal_configuration.copy()
        del raw[deleted]

        with self.assertRaises(config.ConfigurationError) as ctx:
            config.normalise(raw)
        self.assertIn("Configuration entry '" + deleted + "' is required but "
                      "was not found.", str(ctx.exception))

    def test_insert_default(self):
        """Test that all default values are inserted"""
        ret = config.normalise(self.minimal_configuration)

        for key, entry in config.read_metadata().items():
            self.assertIn(key, ret)
            if not entry.required:
                self.assertEqual(entry.default, ret[key])
