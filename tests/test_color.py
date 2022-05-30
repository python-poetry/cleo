from __future__ import annotations

import os

import pytest

from cleo.color import Color


@pytest.mark.parametrize(
    ["foreground", "background", "options", "expected"],
    [
        ("", "", [], " "),
        ("red", "yellow", [], "\033[31;43m \033[39;49m"),
        ("red", "yellow", ["underline"], "\033[31;43;4m \033[39;49;24m"),
    ],
)
def test_ansi_colors(foreground, background, options, expected):
    color = Color(foreground, background, options)

    assert color.apply(" ") == expected


@pytest.mark.skipif(
    os.getenv("COLORTERM") != "truecolor", reason="True color not supported"
)
@pytest.mark.parametrize(
    ["foreground", "background", "options", "expected"],
    [
        ("#fff", "#000", [], "\033[38;2;255;255;255;48;2;0;0;0m \033[39;49m"),
        ("#ffffff", "#000000", [], "\033[38;2;255;255;255;48;2;0;0;0m \033[39;49m"),
    ],
)
def test_true_color_support(foreground, background, options, expected):
    color = Color(foreground, background, options)

    assert color.apply(" ") == expected


@pytest.mark.parametrize(
    ["foreground", "background", "options", "expected"],
    [
        ("#f00", "#ff0", [], "\033[31;43m \033[39;49m"),
        ("#c0392b", "#f1c40f", [], "\033[31;43m \033[39;49m"),
    ],
)
def test_degrade_true_colors(foreground, background, options, expected, environ):
    os.environ["COLORTERM"] = ""

    color = Color(foreground, background, options)

    assert color.apply(" ") == expected
