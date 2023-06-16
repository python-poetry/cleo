from __future__ import annotations

import os

from typing import TYPE_CHECKING

import pytest

from cleo.terminal import Terminal


if TYPE_CHECKING:
    from pytest_mock import MockerFixture


def test_size() -> None:
    terminal = Terminal()
    w, h = terminal.size
    assert terminal.width == w

    terminal = Terminal(width=99, height=101)
    w, h = terminal.size
    assert w == 99 and h == 101


@pytest.mark.parametrize(
    "columns_env_value, init_value, expected",
    (
        ("314", None, 314),
        ("200", 40, 40),
        ("random", 40, 40),
        ("random", None, 80),
    ),
)
def test_columns_env(
    mocker: MockerFixture, columns_env_value: str, init_value: int | None, expected: int
) -> None:
    mocker.patch.dict(os.environ, {"COLUMNS": columns_env_value}, clear=False)
    console = Terminal(width=init_value)
    assert console.width == expected


@pytest.mark.parametrize(
    "lines_env_value, init_value, expected",
    (
        ("314", None, 314),
        ("200", 40, 40),
        ("random", 40, 40),
        ("random", None, 25),
    ),
)
def test_lines_env(
    mocker: MockerFixture, lines_env_value: str, init_value: int | None, expected: int
) -> None:
    mocker.patch.dict(os.environ, {"LINES": lines_env_value}, clear=False)
    console = Terminal(height=init_value)
    assert console.height == expected
