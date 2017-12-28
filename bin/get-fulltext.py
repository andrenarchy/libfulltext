#!/usr/bin/env python3

import libfulltext
from libfulltext.config import Config


def main():
    config = Config()
    libfulltext.getFulltext(config["publishers"],
                            'doi:10.1016/j.physletb.2017.11.066')


if __name__ == '__main__':
    main()
