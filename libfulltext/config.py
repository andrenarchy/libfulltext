import os
import yaml

""" Default location for the configuration file"""
DEFAULT_CONFIG_PATH = "~/.config/libfulltext/config.yaml"


class Config(dict):
    def __setdefault(self):
        self.setdefault("publishers", dict())
        self["publishers"].setdefault("elsevier", dict())
        self["publishers"].setdefault("springer", dict())

    def __init__(self, path=DEFAULT_CONFIG_PATH):
        path = os.path.expanduser(path)

        with open(path, "r") as f:
            cfg_raw = yaml.safe_load(f)
        self.update(cfg_raw)
        self.__setdefault()
        self.path = path

    def save(self, path=None):
        if path is None:
            path = self.path
        with open(path, "w") as f:
            yaml.safe_dump(dict(self), f)
