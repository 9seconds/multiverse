#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function

import argparse
import gzip
import os
import os.path
import sys
import tempfile

import multiverse.utils


GROK_NAMESPACE = "multiverse.grok"
LAST_FILENAME = "mvgrok.gz"


def get_last_filename():
    return os.path.join(tempfile.gettempdir(), LAST_FILENAME)


def main():
    parser = get_parser()
    options = parser.parse_args()

    plugin = multiverse.utils.get_plugin(GROK_NAMESPACE, options.function)
    grok = plugin(options.timestamp_columns, options.message_column)

    if options.repeat_last:
        return repeat_last()
    else:
        return process_new(grok)


def repeat_last():
    try:
        with gzip.open(get_last_filename(), "r") as filefp:
            for line in filefp:
                print(line)
    except Exception:
        return os.EX_NOINPUT


def process_new(grok):
    try:
        last_filefp = gzip.open(get_last_filename(), "w")
    except Exception:
        last_filefp = None

    try:
        for line in sys.stdin:
            result = grok.recognize(line)
            printable = "{0}\t{1}\t{2}".format(
                result.timestamp,
                result.filename,
                result.line)
            print(printable)
            if last_filefp:
                print(printable, file=last_filefp)
    finally:
        if last_filefp:
            last_filefp.close()


def get_parser():
    parser = argparse.ArgumentParser()

    return parser


if __name__ == "__main__":
    sys.exit(main())
