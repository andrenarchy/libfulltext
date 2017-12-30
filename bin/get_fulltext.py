#!/usr/bin/env python3

"""get_fulltext CLI command"""

import libfulltext
from libfulltext.config import Config

def main():
    """Gets fulltexts for prefixed identifiers"""
    config = Config()
    libfulltext.get_fulltext('doi:10.1016/j.physletb.2017.11.066',
                             '/tmp/libfulltext',
                             config
                            )

if __name__ == '__main__':
    main()
