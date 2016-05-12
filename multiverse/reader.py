# -*- coding: utf-8 -*-


import sys
import os.path

import sortedcontainers

import datetime
import multiverse.line


class Reader(object):

    def consume(self, stream):
        parsed = sortedcontainers.SortedList(key=lambda line: line.timestamp)

        for line in stream:
            filename, timestamp, content = self.grok(line)
            created_line = multiverse.line.Line(filename, timestamp, content)
            parsed.add(created_line)

        return parsed
