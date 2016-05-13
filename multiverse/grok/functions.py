# -*- coding: utf-8 -*-


import collections
import re
import time

import dateutil.parser


GrokResult = collections.namedtuple(
    "GrokResult", ["filename", "timestamp", "line"])


class Grok(object):

    CONTROL_SEQUENCE_REGEXP = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")
    # https://en.wikipedia.org/wiki/ANSI_escape_code#CSI_codes

    def __init__(self, timestamp_columns=None, message_column=None):
        self.timestamp_columns = timestamp_columns or []
        self.message_column = message_column or 0

    def recognize(self, line):
        chunks = self.CONTROL_SEQUENCE_REGEXP.sub("", line).strip().split()

        filename = self.extract_filename(chunks)
        timestamp = self.extract_timestamp(chunks)
        message = self.extract_message(chunks)

        return GrokResult(filename, timestamp, message)

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


class GrepGrok(Grok):

    def __init__(self, timestamp_columns=None, message_column=None):
        super(GrepGrok, self).__init__(timestamp_columns, 1)

    def extract_filename(self, chunks):
        return chunks[0].split(":", 1)[0]
