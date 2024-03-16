import hashlib
import pathlib

import error

from typing import List


class ScriptHandler:
    def __init__(self) -> None:
        self.current_line_index = 0
        self.lines: List[str] = []

    @property
    def is_loaded(self):
        return len(self.lines) > 0

    @property
    def previous_line(self):
        if not self.is_loaded:
            return ""
        if self.current_line_index == 0:
            return "< BEGIN SCRIPT >"
        return self.lines[self.current_line_index - 1]

    @property
    def current_line(self):
        if not self.is_loaded:
            return ""
        return self.lines[self.current_line_index]

    @property
    def current_line_hash(self):
        if len(self.lines) < 1:
            raise error.NaratorlyError("Empty Script")
        return hashlib.md5(self.current_line.encode("utf-8")).hexdigest()[0:16]

    @property
    def next_line(self):
        if not self.is_loaded:
            return ""
        if self.current_line_index >= len(self.lines) - 1:
            return "< END SCRIPT >"
        return self.lines[self.current_line_index + 1]

    def load_script(self, lines: List[str]):
        self.lines = []
        for line in lines:
            tmp = line.lstrip().rstrip()
            if len(tmp) > 0 and not tmp[0] == "#":
                self.lines.append(tmp)

    def load_previous_line(self):
        if len(self.lines) < 1:
            return
        self.current_line_index = (self.current_line_index - 1) % len(self.lines)

    def load_next_line(self):
        if len(self.lines) < 1:
            return
        self.current_line_index = (self.current_line_index + 1) % len(self.lines)
