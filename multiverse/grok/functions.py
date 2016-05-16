# -*- coding: utf-8 -*-


import collections
import re
import time

import dateutil.parser


GrokResult = collections.namedtuple(
    "GrokResult", ["timestamp", "filename", "line"])


class Grok(object):

    CONTROL_SEQUENCE_REGEXP = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")
    # https://en.wikipedia.org/wiki/ANSI_escape_code#CSI_codes

    MESSAGE_COLUMN = 0
    TIMESTAMP_COLUMNS = []

    def __init__(self, message_column=None, timestamp_columns=None):
        self.message_column = message_column
        if self.message_column is None:
            self.message_column = self.MESSAGE_COLUMN

        self.timestamp_columns = timestamp_columns
        if self.timestamp_columns is None:
            self.timestamp_columns = self.TIMESTAMP_COLUMNS

    def recognize(self, line):
        chunks = self.CONTROL_SEQUENCE_REGEXP.sub("", line).strip().split()

        filename = self.extract_filename(chunks)
        timestamp = self.extract_timestamp(chunks)
        message = self.extract_message(chunks)

        return GrokResult(timestamp, filename, message)

    def extract_filename(self, chunks):
        return ""

    def extract_message(self, chunks):
        return " ".join(chunks[self.message_column:])

    def extract_timestamp(self, chunks):
        if not self.timestamp_columns:
            return 0

        timestamp = " ".join(chunks[num] for num in self.timestamp_columns)
        timestamp = self.parse_timestamp(timestamp)

        return timestamp

    def parse_timestamp(self, line):
        if line.isdigit():  # unix timestamp
            return int(line)

        parsed = dateutil.parser.parse(line, fuzzy=True)
        if hasattr(parsed, "timestamp"):
            parsed = parsed.timestamp()
        else:
            parsed = time.mktime(parsed.timetuple()) + parsed.microsecond / 1e6
        parsed = int(round(parsed * 1000))

        return parsed


class NoneGrok(Grok):
    pass


class GrepGrok(Grok):

    MESSAGE_COLUMN = 1

    def __init__(self, message_column=None, timestamp_columns=None):
        super(GrepGrok, self).__init__(message_column, timestamp_columns)

    def extract_filename(self, chunks):
        return chunks[0].split(":", 1)[0]
