# -*- coding: utf-8 -*-


import copy
import csv
import logging
import logging.config

import pkg_resources
import unicodecsv


LOG_NAMESPACE = "multiverse"

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "debug": {
            "format": "[%(levelname)s] %(name)30s:%(lineno)d :: %(message)s"
        },
        "simple": {
            "format": "%(message)s"
        },
        "verbose": {
            "format": "[%(levelname)s] %(message)s"
        }
    },
    "handlers": {
        "stderr": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "verbose"
        }
    },
    "loggers": {
        LOG_NAMESPACE: {
            "handlers": ["stderr"],
            "level": "DEBUG",
            "propagate": True
        }
    }
}


csv.register_dialect(
    LOG_NAMESPACE,
    delimiter=",",
    doublequote=True,
    lineterminator="\n",
    quotechar='"',
    quoting=csv.QUOTE_ALL,
    skipinitialspace=False)


def logger(namespace):
    return logging.getLogger(LOG_NAMESPACE + "." + namespace)


def configure_logging(debug=False):
    config = copy.deepcopy(LOG_CONFIG)

    for handler in config["handlers"].values():
        handler["level"] = "DEBUG" if debug else "ERROR"
        handler["formatter"] = "debug" if debug else "verbose"

    logging.config.dictConfig(config)


def all_plugins(group):
    plugins = {}

    for plugin in pkg_resources.iter_entry_points(group):
        plugins[plugin.name] = plugin

    return plugins


def make_csv_reader(filefp):
    return unicodecsv.reader(filefp, dialect=LOG_NAMESPACE)


def make_csv_writer(filefp):
    return unicodecsv.writer(filefp, dialect=LOG_NAMESPACE)
