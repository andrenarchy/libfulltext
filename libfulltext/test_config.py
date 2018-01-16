# copyright © 2018 the libfulltext authors (see AUTHORS.md and LICENSE)
"""Unit tests for config parser"""

import io
import os
from unittest import TestCase
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


class ConfigTestEntryParsers(TestCase):
    """Tests the entry parsers"""

    #
    # string parser
    #
    def test_string_empty(self):
        """Test that the default is an empty string"""
        self.assertEqual(config.EntryParsers.string(), "")

    def test_string_string(self):
        """Parsing a string with string changes nothing"""
        self.assertEqual(config.EntryParsers.string("abc"), "abc")

    def test_string_int(self):
        """Parse an int with string"""
        self.assertEqual(config.EntryParsers.string(5), "5")
        self.assertEqual(config.EntryParsers.string(config.EntryParsers.string(5)), "5")

    #
    # directory parser
    #
    def test_directory_empty(self):
        """The default of directory should be the pwd"""
        self.assertEqual(config.EntryParsers.directory(), os.getcwd())

    def test_directory_relative(self):
        """Test if a plain string gives a relative directory"""
        directory = "testDIRR"
        expect = os.path.join(os.getcwd(), directory)
        self.assertEqual(config.EntryParsers.directory(directory), expect)

    def test_directory_absolute(self):
        """Test if an absolute path gives the same directory back"""
        directory = "/testDIRR"
        self.assertEqual(config.EntryParsers.directory(directory), directory)

    def test_directory_tilde(self):
        """Test if tilde expansion works"""
        directory = "~/test"
        expect = os.path.join(os.environ["HOME"], "test")
        self.assertEqual(config.EntryParsers.directory(directory), expect)


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
        Test whether a complete config passes without problems.
        If this test fails it could indicate that the
        MinimalConfiguration class has not been updated.
        """
        config.normalise(self.minimal_configuration)

    def test_detect_missing_required(self):
        """Missing required values should cause an error"""
        deleted = "publishers_elsevier_apikey"

        # Take complete configuration and remove a key
        raw = self.minimal_configuration
        del raw[deleted]

        with self.assertRaises(config.ConfigurationError) as ctx:
            config.normalise(raw)
        self.assertIn("Configuration entry '" + deleted + "' is required but "
                      "was not found.", str(ctx.exception))

    def test_insert_default(self):
        """All default values should be inserted after the call"""
        ret = config.normalise(self.minimal_configuration)

        for key, entry in config.read_metadata().items():
            self.assertIn(key, ret)
            if not entry.required:
                self.assertEqual(entry.default, ret[key])


class ContigTestObtain(TestCase, MinimalConfiguration):
    """
    Test the config.obtain function
    """
    def test_non_existing_file(self):
        """
        The obtain function should skip over non-existent files
        silently (if the requirements regarding the minimial
        configuration are met by the environment variables.)
        """
        with EnvironmentVariables(self.minimal_environment):
            ret = config.obtain("/nonexistent", environment=True)
        self.assertDictContainsSubset(self.minimal_configuration, ret)

    def test_with_environment(self):
        """A key from the config should get overwritten by the environment"""
        key = "publishers_elsevier_apikey"
        env_vars = {"LIBFULLTEXT_PUBLISHERS_ELSEVIER_APIKEY":  "42"}
        with EnvironmentVariables(env_vars):
            ret = config.obtain(self.minimal_configfile, environment=True)
        self.assertEqual("42", ret[key])

    def test_without_environment(self):
        """The environment=False setting should let us ignore the environment"""
        key = "publishers_elsevier_apikey"
        env_vars = {"LIBFULLTEXT_PUBLISHERS_ELSEVIER_APIKEY":  "42"}
        with EnvironmentVariables(env_vars):
            ret = config.obtain(self.minimal_configfile, environment=False)
        self.assertEqual(self.minimal_configuration[key], ret[key])

    def test_empty_contig(self):
        """A fully empty config should raise an error"""

        with self.assertRaises(config.ConfigurationError) as ctx:
            with EnvironmentVariables(dict()):
                empty = io.StringIO("")
                config.obtain(empty, environment=True)
        self.assertIn("No configuration found.", str(ctx.exception))
