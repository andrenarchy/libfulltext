# copyright © 2017 the libfulltext authors (see AUTHORS.md and LICENSE)
"""Config handling module"""

import functools
import os
import yaml

# Default location for the configuration file
DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/libfulltext/config.yaml")

# The prefix to use for the environment variables we care about.
ENVIRONMENT_VARIABLES_PREFIX = "LIBFULLTEXT"


class ConfigurationError(Exception):
    """Error which is thrown whenever parsing the user configuration failed."""


class EntryParsers:
    """
    This class contains the library of configuration entry parsers.

    The parsers follow the following conveniton:
        - They are named exactly like the type into which they parse
        - They get either a single argument, namely the value to parse,
          or none at all. In the latter case they should return a sensible
          'default'.
        - If parsing cannot be done, they should throw a ConfigurationError.
        - The parsers should be idempotent, i.e. running them twice should
          return the same result as running them once, i.e.
          `parser(parser(value)) = parser(value)`
    """
    @staticmethod
    def string(value=""):
        """Convert a raw configuration entry value into a string"""
        return str(value)

    @staticmethod
    def directory(value=""):
        """Convert a raw configuration entry value into a directory path"""
        if not isinstance(value, str):
            raise ConfigurationError("Directory entry needs to be a string")
        elif not os.path.isabs(value):
            return os.path.abspath(os.path.expanduser(value))
        else:
            return value

    # add more entry types by adding a parser here ...


class ConfigEntry:
    # pylint: disable=too-few-public-methods
    """Class for a parsed configuration entry from config_metadata.yaml."""

    def __init__(self, type, description, default=None, required=False):
        # pylint: disable=redefined-builtin
        """
        Initialise a ConfigEntry class

        Args:
            type:          Type of the entry
            description:   A few lines of description
            default:       Default value
            required:      Is this entry required?

        Raises:
            ConfigurationError    if type is an unknown entry type.
        """
        self.type = type
        self.description = description
        self.required = required

        try:
            self.parser = getattr(EntryParsers, self.type)
        except AttributeError:
            raise ConfigurationError("Invalid configuration entry type {}: "
                                     "Type converter not found.".format(self.type))

        # Use supplied default or the default from the parser.
        if default is None:
            self.default = self.parser()
        else:
            self.default = self.parser(default)


@functools.lru_cache()
def read_metadata():
    """
    Read the configuration data file config_metadata.yaml and return a dict
    with the ConfigEntry objects.

    The function caches the obtained metadata dictionary for the lifetime
    of the module implicitly, so calling it many times will not lead
    to excessive I/O.

    Returns:
        dictionary of ConfigEntry objects.

    Raises:
        ValueError   If something goes wrong when parsing the metadata file.
    """
    cfgmeta_file = os.path.join(os.path.dirname(__file__), "config_metadata.yaml")

    with open(cfgmeta_file, "r") as stream:
        cfgmeta_raw = yaml.safe_load(stream)

    cfgmeta = dict()
    for key, entry in cfgmeta_raw.items():
        if not isinstance(entry, dict):
            raise ValueError("Something went wrong when parsing the config metadata "
                             "file '{}'. Expected a dictionary behind entry {}".format(
                                 cfgmeta_file, key))

        if not key.islower():
            # Needed for compatibility with the way we treat environment variables.
            raise ValueError("Configuration entries need to be lower case only. "
                             "Violating entry {} in file {}".format(cfgmeta_file, key))

        if "type" not in entry or "description" not in entry:
            raise ValueError("The keys 'type' and 'description' are required in each "
                             "entry in the config metadata file, but are missing from "
                             "entry {} in {}".format(cfgmeta_file, key))
        cfgmeta[key] = ConfigEntry(**entry)
    return cfgmeta


def parse_file(path):
    """
    Parse a yaml config file and return the raw dictionary
    of configuration options generated from it.

    Args:
        path:       Path to the configuration yaml file
                    or file stream with its content.
    Returns:
        raw parsed configuration dictionary

    Raises:
        ConfigurationError    if an unknown configuration entry occurrs or
                              the value of an configuration entry is not understood.
    """
    if isinstance(path, str):
        with open(path, "r") as file:
            return parse_file(file)

    cfgmeta = read_metadata()
    root = yaml.safe_load(path)

    # Normalise empty configuration file
    if not root:
        return {}

    if not isinstance(root, dict):
        raise ConfigurationError("Error when parsing configuration file {}: "
                                 "Expected top-level datastructure to be a dictionary"
                                 .format(str(path)))

    for key in root:
        if key not in cfgmeta:
            raise ConfigurationError("Error when parsing configuration file {}: "
                                     "Unknown configuration entry '{}'".format(
                                         str(path), key))
        else:
            root[key] = cfgmeta[key].parser(root[key])
    return root


def parse_environment():
    """
    Parse the os environment and return the raw dictionary
    of configuration options generated from it.

    Returns:
        raw parsed configuration dictionary

    Raises:
        ConfigurationError    if an unknown environment variable occurrs or
                              the value of an environment variable is not understood.
    """
    cfgmeta = read_metadata()

    # Parse environment key:
    root = dict()
    for var, value in os.environ.items():
        if not var.startswith(ENVIRONMENT_VARIABLES_PREFIX):
            continue

        key = var[len(ENVIRONMENT_VARIABLES_PREFIX) + 1:].lower()
        if key not in cfgmeta:
            raise ConfigurationError("Cannot associate environment variable '{}' with "
                                     "any configuration entry.".format(var))
        else:
            root[key] = cfgmeta[key].parser(value)
    return root


def normalise(cfg):
    """
    Normalise a raw configuration dictionary
    and return the result.

    This function verifies that the raw dictionary is sensible
    and will bail out if values have the wrong type,
    required values are missing or values are inconsistent.

    Args:
        cfg:    The raw dictionary returned by any of the parse
                functions. This dictionary will be altered during execution.

    Returns:
        parsed configuration dictionary

    Raises:
        ConfigurationError    If a required configuration entry is missing
                              or if the value of an existing entry is invalid
    """
    cfgmeta = read_metadata()
    for key, entry in cfgmeta.items():
        if key in cfg:
            cfg[key] = entry.parser(cfg[key])
        elif not entry.required:
            cfg[key] = entry.default
        else:
            raise ConfigurationError("Configuration entry '{}' is required but was not "
                                     "found. Did you supply it via the configuration "
                                     "file or the environment variables?".format(key))
    return cfg


def obtain(path=DEFAULT_CONFIG_PATH, environment=True):
    """Parse config file or config stream

    Args:
        path:          Path to the configuration yaml file to use.
        environment:   Should the OS environment variables be considered.

    Returns:
        parsed configuration dictionary

    Raises:
        ConfigurationError    If something went wrong when parsing the configuration
    """
    cfg = dict()
    if not isinstance(path, str) or os.path.isfile(path):
        # File exists or is a stream
        cfg.update(parse_file(path))
    if environment:
        cfg.update(parse_environment())

    if not cfg:
        raise ConfigurationError("No configuration found. Did you supply a default "
                                 "configuration at '{}' or set the required environment "
                                 "variables? If unsure check the documentation."
                                 "".format(DEFAULT_CONFIG_PATH))
    return normalise(cfg)
