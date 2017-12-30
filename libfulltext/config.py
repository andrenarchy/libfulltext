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
    """
    if isinstance(path, str):
        with open(path, "r") as file:
            return parse(file)
    else:
        return yaml.safe_load(path)
