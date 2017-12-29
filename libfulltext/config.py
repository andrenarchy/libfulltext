"""Config module"""

import os
import yaml

# Default location for the configuration file
DEFAULT_CONFIG_PATH = "~/.config/libfulltext/config.yaml"

class Config(dict):
    """Config dict"""
    def __setdefault(self):
        self.setdefault("publishers", dict())
        self["publishers"].setdefault("elsevier", dict())

    def __init__(self, path=DEFAULT_CONFIG_PATH):
        super(Config, self).__init__()
        path = os.path.expanduser(path)

        with open(path, "r") as file:
            cfg_raw = yaml.safe_load(file)
        self.update(cfg_raw)
        self.__setdefault()
        self.path = path

    def save(self, path=None):
        """Save config to file"""
        if path is None:
            path = self.path
        with open(path, "w") as file:
            yaml.safe_dump(dict(self), file)
