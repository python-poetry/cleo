from __future__ import annotations


class TableCellStyle:
    def __init__(
        self, fg="default", bg="default", options=None, align="left", cell_format=None
    ) -> None:
        self._fg = fg
        self._bg = bg
        self._options = options
        self._align = "left"
        self._cell_format = cell_format

    @property
    def cell_format(self) -> str | None:
        return self._cell_format

    @property
    def tag(self) -> str:
        tag = "<fg={};bg={}"

        if self._options:
            tag += ";options={}".format(",".join(self._options))

        tag += ">"

        return tag

    def pad(self, string: str, length: int, char: str = " ") -> str:
        if self._align == "left":
            return string.rjust(length, char)

        if self._align == "right":
            return string.ljust(length, char)

        return string.center(length, char)
