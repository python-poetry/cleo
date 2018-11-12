# -*- coding: utf-8 -*-

import os
import platform
import struct
import subprocess
import shlex


class Terminal(object):
    """
    Represents the current terminal.
    """

    def __init__(self):
        self._width = None
        self._height = None

    @property
    def width(self):
        width = os.getenv("COLUMNS", "").strip()
        if width:
            return int(width)

        if self._width is None:
            self._init_dimensions()

        return self._width

    @property
    def height(self):
        height = os.getenv("LINES", "").strip()
        if height:
            return int(height)

        if self._height is None:
            self._init_dimensions()

        return self._height

    def _init_dimensions(self):
        current_os = platform.system().lower()
        dimensions = None

        if current_os.lower() == "windows":
            dimensions = self._get_terminal_size_windows()
            if dimensions is None:
                dimensions = self._get_terminal_size_tput()
        elif current_os.lower() in ["linux", "darwin"] or current_os.startswith(
            "cygwin"
        ):
            dimensions = self._get_terminal_size_linux()

        if dimensions is None:
            dimensions = 80, 25

        self._width, self._height = dimensions

    def _get_terminal_size_windows(self):
        try:
            from ctypes import windll, create_string_buffer

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
        except:
            pass

    def _get_terminal_size_tput(self):
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

            return (cols, rows)
        except:
            pass

    def _get_terminal_size_linux(self):
        def ioctl_GWINSZ(fd):
            try:
                import fcntl
                import termios

                cr = struct.unpack("hh", fcntl.ioctl(fd, termios.TIOCGWINSZ, "1234"))
                return cr
            except:
                pass

        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)
            except:
                pass

        if not cr:
            try:
                cr = (os.environ["LINES"], os.environ["COLUMNS"])
            except:
                return None

        return int(cr[1]), int(cr[0])
