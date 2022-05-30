from __future__ import annotations

import os
import platform
import shlex
import struct
import subprocess


class Terminal:
    """
    Represents the current terminal.
    """

    _width = None
    _height = None

    @property
    def width(self) -> int:
        width = os.getenv("COLUMNS", "").strip()
        if width:
            return int(width)

        if self.__class__._width is None:
            self._init_dimensions()

        return self.__class__._width

    @property
    def height(self) -> int:
        height = os.getenv("LINES", "").strip()
        if height:
            return int(height)

        if self.__class__._height is None:
            self._init_dimensions()

        return self.__class__._height

    @classmethod
    def _init_dimensions(cls) -> None:
        current_os = platform.system().lower()
        dimensions = None

        if current_os.lower() == "windows":
            dimensions = cls._get_terminal_size_windows()
            if dimensions is None:
                dimensions = cls._get_terminal_size_tput()
        elif current_os.lower() in ["linux", "darwin"] or current_os.startswith(
            "cygwin"
        ):
            dimensions = cls._get_terminal_size_linux()

        if dimensions is None:
            dimensions = 80, 25

        # Ensure we have a valid width
        if dimensions[0] <= 0:
            dimensions = 80, dimensions[1]

        cls._width, cls._height = dimensions

    @classmethod
    def _get_terminal_size_windows(cls) -> tuple[int, int] | None:
        try:
            from ctypes import create_string_buffer
            from ctypes import windll

            # stdin handle is -10
            # stdout handle is -11
            # stderr handle is -12
            h = windll.kernel32.GetStdHandle(-12)
            csbi = create_string_buffer(22)
            res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
            if res:
                (
                    bufx,
                    bufy,
                    curx,
                    cury,
                    wattr,
                    left,
                    top,
                    right,
                    bottom,
                    maxx,
                    maxy,
                ) = struct.unpack("hhhhHhhhhhh", csbi.raw)
                sizex = right - left + 1
                sizey = bottom - top + 1
                return sizex, sizey
        except Exception:
            return

    @classmethod
    def _get_terminal_size_tput(cls) -> tuple[int, int] | None:
        # get terminal width
        # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
        try:
            cols = int(
                subprocess.check_output(
                    shlex.split("tput cols"), stderr=subprocess.STDOUT
                )
            )
            rows = int(
                subprocess.check_output(
                    shlex.split("tput lines"), stderr=subprocess.STDOUT
                )
            )

            return cols, rows
        except Exception:
            pass

    @classmethod
    def _get_terminal_size_linux(cls) -> tuple[int, int] | None:
        def ioctl_GWINSZ(fd):
            try:
                import fcntl
                import termios

                cr = struct.unpack("hh", fcntl.ioctl(fd, termios.TIOCGWINSZ, "1234"))
                return cr
            except Exception:
                pass

        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)
            except Exception:
                pass

        if not cr:
            try:
                cr = (os.environ["LINES"], os.environ["COLUMNS"])
            except Exception:
                return

        return int(cr[1]), int(cr[0])
