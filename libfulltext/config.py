# copyright © 2017 the libfulltext authors (see AUTHORS.md and LICENSE)
"""Config handling module"""

import collections
import os
import yaml

# Default location for the configuration file
DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/libfulltext/config.yaml")

# Named tuple for the parsed entries of config_metadata.yaml
ConfigEntry = collections.namedtuple("ConfigEntry",
                                     ["type", "description", "path",
                                      "default", "required"])
ConfigEntry.__new__.__defaults__ = (None, False)


def read_metadata():
    """
    Read the configuration data file config_metadata.yaml and return a dict
    with the ConfigEntry objects.

    Returns:
        dictionary of ConfigEntry objects.
    """
    cfgdata_file = os.path.join(os.path.dirname(__file__), "config_metadata.yaml")

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
                raise ValueError("Something went wrong when parsing the config_metadata "
                                 "file '{}'. Expected a dictionary at path {}".format(
                                     cfgdata_file, fullpath))
            if "_" in key:
                # This is needed for compatibility with the way the environment
                # variables are treated as configuration entries
                raise ValueError("None of the configuration entries in the "
                                 "read_config_metadata.yaml may contain the character "
                                 "'_'. Violating path: {}".format(fullpath))

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
CONFIG_METADATA = read_metadata()


def __check_unknown(raw_dict, config_metadata, path=""):
    """Check for unknown entries in the raw dictionary"""
    for key, value in raw_dict.items():
        fullpath = path + "/" + key
        if isinstance(value, dict):
            __check_unknown(raw_dict[key], config_metadata.get(key, dict()),
                            path=fullpath)
        if key not in config_metadata:
            raise ValueError("Unknown config entry: {}".format(fullpath))


def __insert_defaults(raw_dict, config_metadata, path=""):
    """
    Check all required config entries are present in the raw dictionary
    and insert default values where appropriate.
    """
    for key, value in config_metadata.items():
        fullpath = path + "/" + key
        if isinstance(value, dict):
            __insert_defaults(raw_dict.get(key, dict()), config_metadata[key],
                              path=fullpath)
        elif key not in raw_dict:
            if value.required:
                raise ValueError("Required config entry {} not present".format(fullpath))
            else:
                raw_dict[key] = value.default


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

    ret = yaml.safe_load(path)
    try:
        __check_unknown(ret, CONFIG_METADATA)
        # TODO More checks, e.g. type
    except (ValueError, TypeError) as exc:
        raise ValueError("Error when parsing configuration file {}: "
                         "{}".format(str(path), str(exc)))
    return ret


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

    try:
        __check_unknown(root, CONFIG_METADATA)
        # TODO More checks, e.g. type
    except (TypeError, ValueError) as exc:
        raise ValueError("Error when parsing environment variables: "
                         "{}".format(str(exc)))
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
    __check_unknown(raw_dict, CONFIG_METADATA)
    # TODO More checks e.g. Type
    __insert_defaults(raw_dict, CONFIG_METADATA)
    return raw_dict


def obtain(path=DEFAULT_CONFIG_PATH, consider_env=True):
    """Parse config file or config stream

    Args:
        path:           Path to the configuration yaml file to use.
        consider_env:   Should the OS environment variables be considered.

    Returns:
        parsed configuration dictionary

    Raises:
        ValueError if any of the configs contains invalid values
        TypeError if any of the configs contains values of the wrong type
    """
    cfg = dict()

    if not isinstance(path, str) or os.path.isfile(path):
        # File is a stream ore exists
        merge_config_into(parse_file(path), cfg)

    if consider_env:
        merge_config_into(parse_env(), cfg)

    if not cfg:
        # No configuration entries found anywhere.
        raise ValueError("No configuration found. Did you supply a default configuration "
                         "at {} or set the required environment "
                         "variables?".format(DEFAULT_CONFIG_PATH))

    return normalise(cfg)
