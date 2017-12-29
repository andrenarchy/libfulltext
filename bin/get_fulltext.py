#!/usr/bin/env python3

"""get_fulltext CLI command"""

import libfulltext
from libfulltext.config import Config

def main():
    """Gets fulltexts for prefixed identifiers"""
    config = Config()
    libfulltext.get_fulltext(config,
                             'doi:10.1016/j.physletb.2017.11.066')

if __name__ == '__main__':
    main()
