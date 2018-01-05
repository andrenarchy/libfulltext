# copyright © 2017 the libfulltext authors (see AUTHORS.md and LICENSE)
"""Config handling module"""

import collections
import functools
import os
import yaml

# Default location for the configuration file
DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/libfulltext/config.yaml")

# The prefix to use for the environment variables we care about.
ENVIRONMENT_VARIABLES_PREFIX = "LIBFULLTEXT"

# Named tuple for the parsed entries of config_metadata.yaml
# type: Type of the entry
# description: Description of the entry
# default: Default value for this entry
# required: Is this entry required
ConfigEntry = collections.namedtuple("ConfigEntry",
                                     ["type", "description", "default", "required"])
ConfigEntry.__new__.__defaults__ = (None, False)


class ConfigurationError(Exception):
    """Error which is thrown whenever parsing the user configuration failed."""


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

        # TODO Perhaps the default value needs to be parsed here!

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
    """
    if isinstance(path, str):
        with open(path, "r") as file:
            return parse_file(file)

    cfgmeta = read_metadata()
    root = yaml.safe_load(path)

    for key in root:
        if key not in cfgmeta:
            raise ConfigurationError("Error when parsing configuration file {}: "
                                     "Unknown configuration entry '{}'".format(
                                         str(path), key))
        # TODO More checks, e.g. type
    return root


def parse_environment():
    """
    Parse the os environment and return the raw dictionary
    of configuration options generated from it.

    Returns:
        raw parsed configuration dictionary
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

        # TODO parse according to type
        root[key] = value
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
        ValueError if the raw dictionary contains invalid values
        TypeError if the raw dictionary contains values of the wrong type
    """
    cfgmeta = read_metadata()
    for key, entry in cfgmeta.items():
        if key in cfg:
            pass  # TODO More checks, e.g. type
        elif not entry.required:
            cfg[key] = entry.default
        else:
            raise ConfigurationError("Configuration entry {} is required but was not "
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
        ValueError if any of the configs contains invalid values
        TypeError if any of the configs contains values of the wrong type
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
