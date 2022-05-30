from __future__ import annotations

import re
import threading
import time

from contextlib import contextmanager
from typing import TYPE_CHECKING

from cleo._utils import format_time
from cleo.io.io import IO


if TYPE_CHECKING:
    from cleo.io.outputs.output import Output


class ProgressIndicator:
    """
    A process indicator.
    """

    NORMAL = " {indicator} {message}"
    NORMAL_NO_ANSI = " {message}"
    VERBOSE = " {indicator} {message} ({elapsed:6s})"
    VERBOSE_NO_ANSI = " {message} ({elapsed:6s})"
    VERY_VERBOSE = " {indicator} {message} ({elapsed:6s})"
    VERY_VERBOSE_NO_ANSI = " {message} ({elapsed:6s})"

    def __init__(
        self,
        io: IO | Output,
        fmt: str | None = None,
        interval: int = 100,
        values: list[str] | None = None,
    ) -> None:
        if isinstance(io, IO):
            io = io.error_output

        self._io = io

        if fmt is None:
            fmt = self._determine_best_format()

        self._fmt = fmt

        if values is None:
            values = ["-", "\\", "|", "/"]

        if len(values) < 2:
            raise ValueError(
                "The progress indicator must have at least 2 indicator value characters."
            )

        self._interval = interval
        self._values = values

        self._message = None
        self._update_time = None
        self._started = False
        self._current = 0

        self._auto_running = None
        self._auto_thread = None

        self._start_time = None
        self._last_message_length = 0

    @property
    def message(self) -> str | None:
        return self._message

    def set_message(self, message: str | None) -> None:
        self._message = message

        self._display()

    @property
    def current_value(self) -> str:
        return self._values[self._current % len(self._values)]

    def start(self, message: str) -> None:
        if self._started:
            raise RuntimeError("Progress indicator already started.")

        self._message = message
        self._started = True
        self._start_time = time.time()
        self._update_time = self._get_current_time_in_milliseconds() + self._interval
        self._current = 0

        self._display()

    def advance(self) -> None:
        if not self._started:
            raise RuntimeError("Progress indicator has not yet been started.")

        if not self._io.is_decorated():
            return

        current_time = self._get_current_time_in_milliseconds()
        if current_time < self._update_time:
            return

        self._update_time = current_time + self._interval
        self._current += 1

        self._display()

    def finish(self, message: str, reset_indicator: bool = False) -> None:
        if not self._started:
            raise RuntimeError("Progress indicator has not yet been started.")

        if self._auto_thread is not None:
            self._auto_running.set()
            self._auto_thread.join()

        self._message = message

        if reset_indicator:
            self._current = 0

        self._display()
        self._io.write_line("")
        self._started = False

    @contextmanager
    def auto(self, start_message: str, end_message: str):
        """
        Auto progress.
        """
        self._auto_running = threading.Event()
        self._auto_thread = threading.Thread(target=self._spin)

        self.start(start_message)
        self._auto_thread.start()

        try:
            yield self
        except (Exception, KeyboardInterrupt):
            self._io.write_line("")

            self._auto_running.set()
            self._auto_thread.join()

            raise

        self.finish(end_message, reset_indicator=True)

    def _spin(self) -> None:
        while not self._auto_running.is_set():
            self.advance()

            time.sleep(0.1)

    def _display(self) -> None:
        if self._io.is_quiet():
            return

        self._overwrite(
            re.sub(
                r"(?i){([a-z\-_]+)(?::([^}]+))?}", self._overwrite_callback, self._fmt
            )
        )

    def _overwrite_callback(self, matches):
        if hasattr(self, f"_formatter_{matches.group(1)}"):
            text = str(getattr(self, f"_formatter_{matches.group(1)}")())
        else:
            text = matches.group(0)

        return text

    def _overwrite(self, message) -> None:
        """
        Overwrites a previous message to the output.
        """
        if self._io.is_decorated():
            self._io.write("\x0D\x1B[2K")
            self._io.write(message)
        else:
            self._io.write_line(message)

    def _determine_best_format(self):
        decorated = self._io.is_decorated()

        if self._io.is_very_verbose():
            if decorated:
                return self.VERY_VERBOSE

            return self.VERY_VERBOSE_NO_ANSI
        elif self._io.is_verbose():
            if decorated:
                return self.VERY_VERBOSE

            return self.VERBOSE_NO_ANSI

        if decorated:
            return self.NORMAL

        return self.NORMAL_NO_ANSI

    def _get_current_time_in_milliseconds(self) -> int:
        return round(time.time() * 1000)

    def _formatter_indicator(self) -> str:
        return self.current_value

    def _formatter_message(self):
        return self.message

    def _formatter_elapsed(self) -> str:
        return format_time(time.time() - self._start_time)
