from __future__ import annotations

from typing import TYPE_CHECKING

from cleo.ui.progress_indicator import ProgressIndicator


if TYPE_CHECKING:
    from typing import Callable

    from cleo.io.buffered_io import BufferedIO


def test_default_indicator(ansi_io: BufferedIO, sleep: Callable[[float], None]) -> None:
    bar = ProgressIndicator(ansi_io)
    bar.start("Starting...")
    sleep(0.101)
    bar.advance()
    sleep(0.101)
    bar.advance()
    sleep(0.101)
    bar.advance()
    sleep(0.101)
    bar.advance()
    sleep(0.101)
    bar.advance()
    sleep(0.101)
    bar.set_message("Advancing...")
    bar.advance()
    bar.finish("Done...")
    bar.start("Starting Again...")
    sleep(0.101)
    bar.advance()
    bar.finish("Done Again...")
    bar.start("Starting Again...")
    sleep(0.101)
    bar.advance()
    bar.finish("Done Again...", reset_indicator=True)

    output = [
        " - Starting...",
        " \\ Starting...",
        " | Starting...",
        " / Starting...",
        " - Starting...",
        " \\ Starting...",
        " \\ Advancing...",
        " | Advancing...",
        " | Done...",
    ]

    expected = "\x0D\x1B[2K" + "\x0D\x1B[2K".join(output)

    expected += "\n"

    output = [" - Starting Again...", " \\ Starting Again...", " \\ Done Again..."]

    expected += "\x0D\x1B[2K" + "\x0D\x1B[2K".join(output)

    expected += "\n"

    output = [" - Starting Again...", " \\ Starting Again...", " - Done Again..."]

    expected += "\x0D\x1B[2K" + "\x0D\x1B[2K".join(output)

    expected += "\n"

    assert expected == ansi_io.fetch_error()


def test_explicit_format(ansi_io: BufferedIO, sleep: Callable[[float], None]) -> None:
    bar = ProgressIndicator(ansi_io, ProgressIndicator.NORMAL)
    bar.start("Starting...")
    sleep(0.101)
    bar.advance()
    sleep(0.101)
    bar.advance()
    sleep(0.101)
    bar.advance()
    sleep(0.101)
    bar.advance()
    sleep(0.101)
    bar.advance()
    sleep(0.101)
    bar.set_message("Advancing...")
    bar.advance()
    bar.finish("Done...")
    bar.start("Starting Again...")
    sleep(0.101)
    bar.advance()
    bar.finish("Done Again...")
    bar.start("Starting Again...")
    sleep(0.101)
    bar.advance()
    bar.finish("Done Again...", reset_indicator=True)

    output = [
        " - Starting...",
        " \\ Starting...",
        " | Starting...",
        " / Starting...",
        " - Starting...",
        " \\ Starting...",
        " \\ Advancing...",
        " | Advancing...",
        " | Done...",
    ]

    expected = "\x0D\x1B[2K" + "\x0D\x1B[2K".join(output)

    expected += "\n"

    output = [" - Starting Again...", " \\ Starting Again...", " \\ Done Again..."]

    expected += "\x0D\x1B[2K" + "\x0D\x1B[2K".join(output)

    expected += "\n"

    output = [" - Starting Again...", " \\ Starting Again...", " - Done Again..."]

    expected += "\x0D\x1B[2K" + "\x0D\x1B[2K".join(output)

    expected += "\n"

    assert expected == ansi_io.fetch_error()
