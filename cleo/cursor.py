import sys

from typing import Optional
from typing import TextIO
from typing import Union

from cleo.io.io import IO
from cleo.io.outputs.output import Output


class Cursor:
    def __init__(self, io: Union[IO, Output], input: Optional[TextIO] = None) -> None:
        if isinstance(io, IO):
            io = io.output

        self._output = io

        if input is None:
            input = sys.stdin

        self._input = input

    def move_up(self, lines: int = 1) -> "Cursor":
        self._output.write("\x1b[{}A".format(lines))

        return self

    def move_down(self, lines: int = 1) -> "Cursor":
        self._output.write("\x1b[{}B".format(lines))

        return self

    def move_right(self, columns: int = 1) -> "Cursor":
        self._output.write("\x1b[{}C".format(columns))

        return self

    def move_left(self, columns: int = 1) -> "Cursor":
        self._output.write("\x1b[{}D".format(columns))

        return self

    def move_to_column(self, column: int) -> "Cursor":
        self._output.write("\x1b[{}G".format(column))

        return self

    def move_to_position(self, column: int, row: int) -> "Cursor":
        self._output.write("\x1b[{};{}H".format(row + 1, column))

        return self

    def save_position(self) -> "Cursor":
        self._output.write("\x1b7")

        return self

    def restore_position(self) -> "Cursor":
        self._output.write("\x1b8")

        return self

    def hide(self) -> "Cursor":
        self._output.write("\x1b[?25l")

        return self

    def show(self) -> "Cursor":
        self._output.write("\x1b[?25h\x1b[?0c")

        return self

    def clear_line(self) -> "Cursor":
        """
        Clears all the output from the current line.
        """
        self._output.write("\x1b[2K")

        return self

    def clear_line_after(self) -> "Cursor":
        """
        Clears all the output from the current line after the current position.
        """
        self._output.write("\x1b[K")

        return self

    def clear_output(self) -> "Cursor":
        """
        Clears all the output from the cursors' current position
        to the end of the screen.
        """
        self._output.write("\x1b[0J")

        return self

    def clear_screen(self) -> "Cursor":
        """
        Clears the entire screen.
        """
        self._output.write("\x1b[2J")

        return self
