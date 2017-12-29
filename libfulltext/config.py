"""Config handling module"""

import os
import yaml

# Default location for the configuration file
DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/libfulltext/config.yaml")


def parse(path=DEFAULT_CONFIG_PATH):
    """Parse config file or config stream"""
    if isinstance(path, str):
        path = os.path.expanduser(path)
        with open(path, "r") as file:
            return parse(file)
    else:
        return yaml.safe_load(path)
