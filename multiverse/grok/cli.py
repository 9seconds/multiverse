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

LOG = multiverse.utils.logger(__name__)
"""Logger."""


def main():
    all_plugins = multiverse.utils.all_plugins(GROK_NAMESPACE)
    parser = get_parser(all_plugins)
    options = parser.parse_args()

    multiverse.utils.configure_logging(options.debug)

    LOG.debug("Options are %s", options)
    LOG.debug("Temporary filename is %s", get_last_filename())

    plugin = all_plugins[options.format].load()
    grok = plugin(options.timestamp_columns)

    if options.repeat_last:
        return repeat_last()
    else:
        return process_new(grok)


def get_last_filename():
    return os.path.join(tempfile.gettempdir(), LAST_FILENAME)


def repeat_last():
    try:
        with gzip.open(get_last_filename(), "r") as filefp:
            for line in filefp:
                print(line, end="")
    except Exception as exc:
        LOG.warning("Cannot open file %s: %s", get_last_filename(), exc)
        return os.EX_NOINPUT
    else:
        return os.EX_OK


def process_new(grok):
    try:
        last_filefp = gzip.open(get_last_filename(), "w")
    except Exception as exc:
        LOG.warning("Cannot use %s: %s", get_last_filename(), exc)
        last_filefp = None
        last_csvwriter = None
    else:
        last_csvwriter = multiverse.utils.make_csv_writer(last_filefp)

    stdout_writer = multiverse.utils.make_csv_writer(sys.stdout)
    try:
        for line in sys.stdin:
            LOG.info("Process line %r", line)
            result = grok.recognize(line)
            LOG.debug("Processed result is %s", result)

            stdout_writer.writerow(result)
            if last_csvwriter:
                last_csvwriter.writerow(result)
    except Exception as exc:
        LOG.error("Cannot write result %s: %s", result, exc)
        return os.EX_SOFTWARE
    else:
        return os.EX_OK
    finally:
        if last_filefp:
            last_filefp.close()


def get_parser(plugins):
    parser = argparse.ArgumentParser(
        description=(
            "%(prog)s converts output of your search utility to output,"
            " recognizible by other mv* utilities. Basically all you need is"
            " to pipe your grep/ack/agg outputs into mvgrok."))

    parser.add_argument(
        "-f", "--format",
        help="Format of output to grok. Default is grep.",
        default="grep",
        choices=sorted(plugins.keys()))
    parser.add_argument(
        "-c", "--timestamp-columns",
        help="List of columns which are related to message timestamp.",
        nargs="*",
        type=int,
        default=None)
    parser.add_argument(
        "-l", "--repeat-last",
        help="Output result of last command.",
        action="store_true",
        default=False)
    parser.add_argument(
        "-d", "--debug",
        help="Run in debug mode.",
        action="store_true",
        default=False)

    return parser


if __name__ == "__main__":
    sys.exit(main())
