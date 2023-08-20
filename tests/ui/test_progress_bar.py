from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from cleo.io.outputs.output import Verbosity
from cleo.ui.progress_bar import ProgressBar


if TYPE_CHECKING:
    from typing import Callable

    from cleo.io.buffered_io import BufferedIO


@pytest.fixture()
def bar(io: BufferedIO) -> ProgressBar:
    return ProgressBar(io, min_seconds_between_redraws=0)


@pytest.fixture()
def ansi_bar(ansi_io: BufferedIO) -> ProgressBar:
    return ProgressBar(ansi_io, min_seconds_between_redraws=0)


def generate_output(expected: list[str]) -> str:
    output = ""
    for i, line in enumerate(expected):
        if i:
            count = line.count("\n")

            if count:
                output += f"\x1B[{count}A\x1B[1G\x1b[2K"
            else:
                output += "\x1b[1G\x1b[2K"

        output += line

    return output


def test_multiple_start(ansi_bar: ProgressBar, ansi_io: BufferedIO) -> None:
    ansi_bar.start()
    ansi_bar.advance()
    ansi_bar.start()

    output = [
        "    0 [>---------------------------]",
        "    1 [->--------------------------]",
        "    0 [>---------------------------]",
    ]

    expected = generate_output(output)

    assert expected == ansi_io.fetch_error()


def test_advance(ansi_bar: ProgressBar, ansi_io: BufferedIO) -> None:
    ansi_bar.start()
    ansi_bar.advance()

    output = [
        "    0 [>---------------------------]",
        "    1 [->--------------------------]",
    ]

    expected = generate_output(output)

    assert expected == ansi_io.fetch_error()


def test_advance_with_step(ansi_bar: ProgressBar, ansi_io: BufferedIO) -> None:
    ansi_bar.start()
    ansi_bar.advance(5)

    output = [
        "    0 [>---------------------------]",
        "    5 [----->----------------------]",
    ]

    expected = generate_output(output)

    assert expected == ansi_io.fetch_error()


def test_advance_multiple_times(ansi_bar: ProgressBar, ansi_io: BufferedIO) -> None:
    ansi_bar.start()
    ansi_bar.advance(3)
    ansi_bar.advance(2)

    output = [
        "    0 [>---------------------------]",
        "    3 [--->------------------------]",
        "    5 [----->----------------------]",
    ]

    expected = generate_output(output)

    assert expected == ansi_io.fetch_error()


def test_advance_over_max(ansi_io: BufferedIO) -> None:
    bar = ProgressBar(ansi_io, 10)
    bar.set_progress(9)
    bar.advance()
    bar.advance()

    output = [
        "  9/10 [=========================>--]  90%",
        " 10/10 [============================] 100%",
        " 11/11 [============================] 100%",
    ]

    expected = generate_output(output)

    assert expected == ansi_io.fetch_error()


def test_format(ansi_io: BufferedIO) -> None:
    output = [
        "  0/10 [>---------------------------]   0%",
        " 10/10 [============================] 100%",
    ]

    expected = generate_output(output)

    # max in construct, no format
    ansi_io.clear_error()
    bar = ProgressBar(ansi_io, 10)
    bar.start()
    bar.advance(10)
    bar.finish()

    assert expected == ansi_io.fetch_error()

    # max in start, no format
    ansi_io.clear_error()
    bar = ProgressBar(ansi_io)
    bar.start(10)
    bar.advance(10)
    bar.finish()

    assert expected == ansi_io.fetch_error()

    # max in construct, explicit format before
    ansi_io.clear_error()
    bar = ProgressBar(ansi_io, 10)
    bar.set_format("normal")
    bar.start()
    bar.advance(10)
    bar.finish()

    assert expected == ansi_io.fetch_error()

    # max in start, explicit format before
    ansi_io.clear_error()
    bar = ProgressBar(ansi_io)
    bar.set_format("normal")
    bar.start(10)
    bar.advance(10)
    bar.finish()

    assert expected == ansi_io.fetch_error()


def test_customizations(ansi_io: BufferedIO) -> None:
    bar = ProgressBar(ansi_io, 10, 0)
    bar.set_bar_width(10)
    bar.set_bar_character("_")
    bar.set_empty_bar_character(" ")
    bar.set_progress_character("/")
    bar.set_format(" %current%/%max% [%bar%] %percent:3s%%")
    bar.start()
    bar.advance()

    output = ["  0/10 [/         ]   0%", "  1/10 [_/        ]  10%"]

    expected = generate_output(output)

    assert expected == ansi_io.fetch_error()


def test_display_without_start(ansi_io: BufferedIO) -> None:
    bar = ProgressBar(ansi_io, 50, 0)
    bar.display()

    expected = "  0/50 [>---------------------------]   0%"

    assert ansi_io.fetch_error() == expected


def test_display_with_quiet_verbosity(ansi_io: BufferedIO) -> None:
    ansi_io.set_verbosity(Verbosity.QUIET)
    bar = ProgressBar(ansi_io, 50, 0)
    bar.display()

    assert ansi_io.fetch_error() == ""


def test_finish_without_start(ansi_io: BufferedIO) -> None:
    bar = ProgressBar(ansi_io, 50, 0)
    bar.finish()

    expected = " 50/50 [============================] 100%"

    assert ansi_io.fetch_error() == expected


def test_percent(ansi_io: BufferedIO) -> None:
    bar = ProgressBar(ansi_io, 50, 0)
    bar.start()
    bar.display()
    bar.advance()
    bar.advance()

    output = [
        "  0/50 [>---------------------------]   0%",
        "  1/50 [>---------------------------]   2%",
        "  2/50 [=>--------------------------]   4%",
    ]

    expected = generate_output(output)

    assert expected == ansi_io.fetch_error()


def test_overwrite_with_shorter_line(ansi_io: BufferedIO) -> None:
    bar = ProgressBar(ansi_io, 50, 0)
    bar.set_format(" %current%/%max% [%bar%] %percent:3s%%")
    bar.start()
    bar.display()
    bar.advance()

    # Set shorter format
    bar.set_format(" %current%/%max% [%bar%]")
    bar.advance()

    output = [
        "  0/50 [>---------------------------]   0%",
        "  1/50 [>---------------------------]   2%",
        "  2/50 [=>--------------------------]",
    ]

    expected = generate_output(output)

    assert expected == ansi_io.fetch_error()


def test_set_current_progress(ansi_io: BufferedIO) -> None:
    bar = ProgressBar(ansi_io, 50, 0)
    bar.start()
    bar.display()
    bar.advance()
    bar.set_progress(15)
    bar.set_progress(25)

    output = [
        "  0/50 [>---------------------------]   0%",
        "  1/50 [>---------------------------]   2%",
        " 15/50 [========>-------------------]  30%",
        " 25/50 [==============>-------------]  50%",
    ]

    expected = generate_output(output)

    assert expected == ansi_io.fetch_error()


def test_multibyte_support(ansi_bar: ProgressBar, ansi_io: BufferedIO) -> None:
    ansi_bar.start()
    ansi_bar.set_bar_character("■")
    ansi_bar.advance(3)

    output = [
        "    0 [>---------------------------]",
        "    3 [■■■>------------------------]",
    ]

    expected = generate_output(output)

    assert expected == ansi_io.fetch_error()


def test_clear(ansi_io: BufferedIO) -> None:
    bar = ProgressBar(ansi_io, 50, 0)
    bar.start()
    bar.set_progress(25)
    bar.clear()

    output = [
        "  0/50 [>---------------------------]   0%",
        " 25/50 [==============>-------------]  50%",
        "",
    ]

    expected = generate_output(output)

    assert expected == ansi_io.fetch_error()


def test_percent_not_hundred_before_complete(ansi_io: BufferedIO) -> None:
    bar = ProgressBar(ansi_io, 200, 0)
    bar.start()
    bar.display()
    bar.advance(199)
    bar.advance()

    output = [
        "   0/200 [>---------------------------]   0%",
        " 199/200 [===========================>]  99%",
        " 200/200 [============================] 100%",
    ]

    expected = generate_output(output)

    assert expected == ansi_io.fetch_error()


def test_non_decorated_output(io: BufferedIO) -> None:
    bar = ProgressBar(io, 200, 0)
    bar.start()

    for _ in range(200):
        bar.advance()

    bar.finish()

    expected = "\n".join(
        [
            "   0/200 [>---------------------------]   0%",
            "  20/200 [==>-------------------------]  10%",
            "  40/200 [=====>----------------------]  20%",
            "  60/200 [========>-------------------]  30%",
            "  80/200 [===========>----------------]  40%",
            " 100/200 [==============>-------------]  50%",
            " 120/200 [================>-----------]  60%",
            " 140/200 [===================>--------]  70%",
            " 160/200 [======================>-----]  80%",
            " 180/200 [=========================>--]  90%",
            " 200/200 [============================] 100%",
        ]
    )

    assert expected == io.fetch_error()


def test_multiline_format(ansi_io: BufferedIO) -> None:
    bar = ProgressBar(ansi_io, 3, 0)
    bar.set_format("%bar%\nfoobar")

    bar.start()
    bar.advance()
    bar.clear()
    bar.finish()

    output = [
        ">---------------------------\nfoobar",
        "=========>------------------\nfoobar",
        "\n",
        "============================\nfoobar",
    ]

    expected = generate_output(output)

    assert expected == ansi_io.fetch_error()


def test_regress(ansi_bar: ProgressBar, ansi_io: BufferedIO) -> None:
    ansi_bar.start()
    ansi_bar.advance()
    ansi_bar.advance()
    ansi_bar.advance(-1)

    output = [
        "    0 [>---------------------------]",
        "    1 [->--------------------------]",
        "    2 [-->-------------------------]",
        "    1 [->--------------------------]",
    ]

    expected = generate_output(output)

    assert expected == ansi_io.fetch_error()


def test_regress_with_steps(ansi_bar: ProgressBar, ansi_io: BufferedIO) -> None:
    ansi_bar.start()
    ansi_bar.advance(4)
    ansi_bar.advance(4)
    ansi_bar.advance(-2)

    output = [
        "    0 [>---------------------------]",
        "    4 [---->-----------------------]",
        "    8 [-------->-------------------]",
        "    6 [------>---------------------]",
    ]

    expected = generate_output(output)

    assert expected == ansi_io.fetch_error()


def test_regress_multiple_times(ansi_bar: ProgressBar, ansi_io: BufferedIO) -> None:
    ansi_bar.start()
    ansi_bar.advance(3)
    ansi_bar.advance(3)
    ansi_bar.advance(-1)
    ansi_bar.advance(-2)

    output = [
        "    0 [>---------------------------]",
        "    3 [--->------------------------]",
        "    6 [------>---------------------]",
        "    5 [----->----------------------]",
        "    3 [--->------------------------]",
    ]

    expected = generate_output(output)

    assert expected == ansi_io.fetch_error()


def test_regress_below_min(ansi_io: BufferedIO) -> None:
    bar = ProgressBar(ansi_io, 10, 0)
    bar.set_progress(1)
    bar.advance(-1)
    bar.advance(-1)

    output = [
        "  1/10 [==>-------------------------]  10%",
        "  0/10 [>---------------------------]   0%",
    ]

    expected = generate_output(output)

    assert expected == ansi_io.fetch_error()


def test_overwrite_with_section_output(ansi_io: BufferedIO) -> None:
    bar = ProgressBar(ansi_io.section(), 50, 0)
    bar.start()
    bar.display()
    bar.advance()
    bar.advance()

    output = [
        "  0/50 [>---------------------------]   0%",
        "  1/50 [>---------------------------]   2%",
        "  2/50 [=>--------------------------]   4%",
    ]

    expected = "\n\x1b[1A\x1b[0J".join(output) + "\n"

    assert expected == ansi_io.fetch_output()


def test_overwrite_multiple_progress_bars_with_section_outputs(
    ansi_io: BufferedIO,
) -> None:
    output1 = ansi_io.section()
    output2 = ansi_io.section()

    bar1 = ProgressBar(output1, 50, 0)
    bar2 = ProgressBar(output2, 50, 0)

    bar1.start()
    bar2.start()

    bar2.advance()
    bar1.advance()

    output = [
        "  0/50 [>---------------------------]   0%",
        "  0/50 [>---------------------------]   0%",
        "\x1b[1A\x1b[0J  1/50 [>---------------------------]   2%",
        "\x1b[2A\x1b[0J  1/50 [>---------------------------]   2%",
        "\x1b[1A\x1b[0J  1/50 [>---------------------------]   2%",
        "  1/50 [>---------------------------]   2%",
    ]

    expected = "\n".join(output) + "\n"

    assert expected == ansi_io.fetch_output()


def test_min_and_max_seconds_between_redraws(
    ansi_bar: ProgressBar, ansi_io: BufferedIO, sleep: Callable[[float], None]
) -> None:
    ansi_bar.min_seconds_between_redraws(0.5)
    ansi_bar.max_seconds_between_redraws(2 - 1)

    ansi_bar.start()
    ansi_bar.set_progress(1)
    sleep(1)
    ansi_bar.set_progress(2)
    sleep(2)
    ansi_bar.set_progress(3)

    output = [
        "    0 [>---------------------------]",
        "    2 [->--------------------------]",
        "    3 [-->-------------------------]",
    ]

    expected = generate_output(output)

    assert expected == ansi_io.fetch_error()
