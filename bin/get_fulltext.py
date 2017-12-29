#!/usr/bin/env python3

"""get_fulltext CLI command"""

import click
import libfulltext
import libfulltext.config
import select

# Settings for click
CLICK_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CLICK_SETTINGS)
@click.option("-c", "--config", default=libfulltext.config.DEFAULT_CONFIG_PATH,
              type=click.File())
@click.argument("prefixed_ids", nargs=-1, default=None)
@click.option("-f", "--prefixed-id-file", default="-", type=click.File())
def get_fulltext(config, prefixed_ids, prefixed_id_file):
    # Setup the config dictionary:
    cfg = libfulltext.config.parse(config)

    if prefixed_ids:
        # If we have IDs on the command line, we do not want
        # to keep blocking, waiting from stdin.
        rlist, _, _ = select.select([prefixed_id_file], [], [], 0)
        if rlist:
            # If an element is in the rlist, the user supplied
            # both a stream on stdin as well as some ids on the commandline,
            # which we do not support.
            raise SystemExit("Either you provide prefixed IDs on STDIN, a file "
                             "via --prefixed-id-file or alternatively directly "
                             "on the commandline. A combination is not allowed.")
        else:
            # Close the input to stop the blocking stdin.
            prefixed_id_file.close()
    else:
        prefixed_ids = prefixed_id_file.read().split("\n")

    for prfid in prefixed_ids:
        libfulltext.get_fulltext(prfid, "/tmp/libfulltext", cfg)

if __name__ == '__main__':
    get_fulltext()
