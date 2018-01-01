"""Config handling module"""

import os
import yaml

# Default location for the configuration file
DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/libfulltext/config.yaml")


def parse(path=DEFAULT_CONFIG_PATH):
    """Parse config file or config stream

    Args:
        path:       Path to the configuration yaml file
                    or file stream with its content.
    Returns:
        parsed configuration dictionary
    """
    if isinstance(path, str):
        with open(path, "r") as file:
            return parse(file)
    else:
        cfg = yaml.safe_load(path)

        # Insert defaults
        cfg.setdefault("storage", dict())
        cfg["storage"].setdefault("fulltext", os.path.abspath("fulltext"))
        return cfg
