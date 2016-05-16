#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import os
import sys

import multiverse.utils


EXPORT_NAMESPACE = "multiverse.export"

LOG = multiverse.utils.logger(__name__)


def main():
    all_plugins = multiverse.utils.all_plugins(EXPORT_NAMESPACE)
    parser = get_parser(all_plugins)
    options = parser.parse_args()

    multiverse.utils.configure_logging(options.debug)

    LOG.debug("Options are %s", options)

    return os.EX_OK


def get_parser(plugins):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d", "--debug",
        help="Run in debug mode.",
        action="store_true",
        default=False)
    parser.add_argument(
        "-f", "--format",
        help="Formatter to use for export. Default is 'csv'.",
        choices=sorted(plugins.keys()),
        default="csv")
    parser.add_argument(
        "-o", "--output",
        help="Output filename. Use '-' for stdout (stdout is default one)",
        default="-")
    parser.add_argument(
        "-b", "--base-timestamp",
        help=(
            "Base timestamp to define time range. If '-r' is set, "
            "then range [s-r; s+r] will be used. If -p if set, "
            "then [b; p] range is used. If nothing is set, then no "
            "limits will be used."),
        default=None)

    bounds = parser.add_mutually_exclusive_group()
    bounds.add_argument(
        "-r", "--range",
        help="Time range for base timestamp in seconds. Default is 1 second.",
        type=int)
    bounds.add_argument(
        "-p", "--other-timestamp",
        help=(
            "Complement timestamp for base timestamp. Both timestamps "
            "make inclusive range."))

    parser.add_argument(
        "filenames",
        metavar="FILENAME",
        help=(
            "Filenames from mvgrok to use for export. If nothing is "
            "set or '-' is filename, then stdin is used."),
        nargs="*")

    return parser


if __name__ == "__main__":
    sys.exit(main())
