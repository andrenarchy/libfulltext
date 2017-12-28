#!/usr/bin/env python3
import yaml
from libfulltext.config import DEFAULT_CONFIG_PATH
import os


def dump_default_config(path):
    path = os.path.realpath(os.path.expanduser(path))
    if os.path.exists(path):
        raise SystemExit("Config already exists. Bailing out.")

    elsevier_api_key = input("Enter your Elsevier API key: ")
    cfg = dict()
    cfg["publishers"] = dict()
    cfg["publishers"]["elsevier"] = dict()
    cfg["publishers"]["elsevier"]["apikey"] = elsevier_api_key

    dirname = os.path.dirname(path)
    os.makedirs(dirname, exist_ok=True)
    with open(path, "w") as f:
        yaml.safe_dump(cfg, f)


def main():
    path = DEFAULT_CONFIG_PATH
    dump_default_config(path)
    print()
    print("Dumped default libfulltext config at " + path)


if __name__ == "__main__":
    main()
