# copyright © 2017 the libfulltext authors (see AUTHORS.md and LICENSE)
"""Config handling module"""

import os
import yaml

# Default location for the configuration file
DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/libfulltext/config.yaml")


def parse_file(path=DEFAULT_CONFIG_PATH):
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
            return parse(file)
    else:
        return yaml.safe_load(path)


def parse_env(prefix="LIBFULLTEXT"):
    """
    Parse the os environment and return the raw dictionary
    of configuration options generated from it.

    Args:
        prefix:     The prefix to use for all environment
                    variables used.
    Returns:
        raw parsed configuration dictionary
    """
    root = dict()

    def confdict_insert(envkey, value):
        """Insert an environment variable into the root dict"""
        parts = [p.lower() for p in envkey.split("_")]
        loc = root
        for part in parts[:-1]:
            # Insert a dict, if not present at the current
            # location
            loc = loc.setdefault(part, dict())
        loc[parts[-1]] = value

    for key, value in os.environ.items():
        if key.startswith(prefix):
            # Strip off prefix and insert
            confdict_insert(key[len(prefix) + 1:], value)
    return root


def merge_config_into(dict_from, dict_to):
    """
    Merge two configuration dictionaries. Dict_to will be update
    with the values of dict_from, recursively replacing values
    if newer versions in dict_from exist.

    Args:
        dict_from     The dictionary to take values from
        dict_to       The dictionary to update into

    Returns:
        dict_to after the merge has performed
    """
    for key, value in dict_from.items():
        if isinstance(value, dict) and key in dict_to:
            merge_config_into(dict_from[key], dict_to[key])
        else:
            dict_to[key] = dict_from[key]
    return dict_to


def normalise(raw_dict):
    """
    Normalise a raw configuration dictionary
    and return the result.

    This function verifies that the raw dictionary is sensible
    and will bail out if values have the wrong type,
    required values are missing or values are inconsistent.

    Args:
        raw_dict:    The raw dictionary returned by any of the parse
                     functions.

    Returns:
        parsed configuration dictionary

    Raises:
        ValueError if the raw dictionary contains invalid values
        TypeError if the raw dictionary contains values of the wrong type
    """
    # TODO read configdata and check for sanity
    raw_dict.setdefault("storage", dict())
    raw_dict["storage"].setdefault("fulltext", os.path.abspath("fulltext"))
    return raw_dict


def parse(path=DEFAULT_CONFIG_PATH):
    """Parse config file or config stream

    Args:
        path:       Path to the configuration yaml file
                    or file stream with its content.
    Returns:
        parsed configuration dictionary
    """
    cfg = parse_file(path)
    merge_config_into(parse_env(), cfg)
    return normalise(cfg)
