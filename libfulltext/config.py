# copyright © 2017 the libfulltext authors (see AUTHORS.md and LICENSE)
"""Config handling module"""

import collections
import os
import yaml

# Default location for the configuration file
DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/libfulltext/config.yaml")

# Named tuple for the parsed entries of configdata.yaml
ConfigEntry = collections.namedtuple("ConfigEntry",
                                     ["type", "description", "path",
                                      "default", "required"])
ConfigEntry.__new__.__defaults__ = (None, False)


def read_configdata():
    """
    Read the configuration data file configdata.yaml and return a dict
    with the ConfigEntry objects.

    Returns:
        dictionary of ConfigEntry objects.
    """
    cfgdata_file = os.path.join(os.path.dirname(__file__), "configdata.yaml")

    def parse_cfgdata(yaml_loc, cfgdata_loc, path=""):
        """Parse the dictionary returned by yaml.safe_load into the
        cfgdata file by recursively parsing each level.

        Args:
            yaml_loc: Points to the current location in the yaml dict
            cfgdata_loc: Points to the current location to place the parsed values
            path: Human-readable path (for error messages)
        """
        for key, value in yaml_loc.items():
            fullpath = path + "/" + key

            if not isinstance(value, dict):
                raise ValueError("Something went wrong when parsing the configdata file "
                                 "'{}'. Expected a dictionary at path {}".format(
                                     cfgdata_file, fullpath))
            if "_" in key:
                # This is needed for compatibility with the way the environment
                # variables are treated as configuration entries
                raise ValueError("None of the configuration entries in the "
                                 "configdata.yaml may contain the character '_'. "
                                 "Violating path: {}".format(fullpath))

            if not key.islower():
                # Similarly needed for compatibility how we treat environment variables.
                raise ValueError("Configuration entries need to be lower case only. "
                                 "Violating path: {}".format(fullpath))

            if "type" in value and "description" in value:
                # The current location of "yaml" is a configuration entry,
                # so make a ConfigEntry out of it.
                cfgdata_loc[key] = ConfigEntry(path=path, **value)
            else:
                # Recurse one level deeper
                parse_cfgdata(value, cfgdata_loc.setdefault(key, dict()),
                              path=fullpath)

    cfgdata = dict()
    with open(cfgdata_file, "r") as stream:
        parse_cfgdata(yaml.safe_load(stream), cfgdata)
    return cfgdata


# Read config data once and cache result
CONFIG_DATA = read_configdata()


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


def obtain(paths=["/etc/libfulltext/config.yaml", DEFAULT_CONFIG_PATH],
           consider_env=True):
    """Parse config file or config stream

    Args:
        paths:          Path to the configuration yaml files
                        or file streams with the configuration contents.
                        The files are parsed in this order and newer values
                        overwrite older ones.
        consider_env:   Should the OS environment variables be considered.

    Returns:
        parsed configuration dictionary

    Raises:
        ValueError if any of the configs contains invalid values
        TypeError if any of the configs contains values of the wrong type
    """
    cfg = dict()
    for path in paths:
        if isinstance(path, str) and not os.path.isfile(path):
            continue  # skip missing files
        merge_config_into(parse_file(path), cfg)
    if consider_env:
        merge_config_into(parse_env(), cfg)

    return normalise(cfg)
