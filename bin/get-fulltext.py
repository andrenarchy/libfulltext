#!/usr/bin/env python3

import libfulltext
import yaml

def main():
    with open('config.yml') as file:
        config = yaml.safe_load(file)
    libfulltext.getFulltext(config, 'doi:10.1016/j.physletb.2017.11.066')

if __name__ == '__main__':
    main()
