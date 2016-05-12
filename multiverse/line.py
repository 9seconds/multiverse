# -*- coding: utf-8 -*-


import textwrap


class Line(object):

    PREFIX_FIRST_LINE = ""
    PREFIX_SUBSEQUENT = "| "
    LENGTH_LINE = 79

    __slots__ = "filename", "timestamp", "line"

    def __init__(self, filename, timestamp, line,
                 prefix_first=PREFIX_FIRST_LINE,
                 prefix_subseq=PREFIX_SUBSEQUENT, line_length=LENGTH_LINE):
        self.filename = filename
        self.timestamp = timestamp
        self.line = line
        self.prefix_first = prefix_first
        self.prefix_subseq = prefix_subseq
        self.line_length = line_length

        self.wrapped_lines = None

    def adjusted(self, length):
        lines = [line.ljust(length) for line in self.lines]

        return lines

    @property
    def lines(self):
        if self.wrapped_lines is not None:
            return self.wrapped_lines

        self.wrapped_lines = textwrap.wrap(
            self.line, self.line_length,
            expand_tabs=True,
            replace_whitespace=True,
            drop_whitespace=True,
            initial_indent=self.prefix_first,
            subsequent_indent=self.prefix_subseq,
            break_long_words=False,
            break_on_hyphens=False)

        return self.wrapped_lines

    @property
    def box_size(self):
        width = max(len(line) for line in self.lines)
        height = len(self.lines)

        return width, height
