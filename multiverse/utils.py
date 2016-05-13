# -*- coding: utf-8 -*-


import pkg_resources


def get_plugin(group, name):
    for plugin in pkg_resources.iter_entry_points(group):
        if plugin.name == name:
            return plugin.load()
