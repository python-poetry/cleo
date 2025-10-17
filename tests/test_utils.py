from __future__ import annotations

import pytest

from cleo._utils import find_similar_names
from cleo._utils import format_time
from cleo._utils import strip_tags
from cleo._utils import wcswidth
from cleo._utils import wcwidth


@pytest.mark.parametrize(
    ["input_secs", "expected"],
    [
        (0.1, "< 1 sec"),
        (1.0, "1 sec"),
        (2.0, "2 secs"),
        (59.0, "59 secs"),
        (60.0, "1 min"),
        (120.0, "2 mins"),
        (3600.0, "1 hr"),
        (7200.0, "2 hrs"),
        (129600.0, "1 day"),
        (129601.0, "2 days"),
        (700000.0, "9 days"),
    ],
)
def test_format_time(input_secs: float, expected: str) -> None:
    assert format_time(input_secs) == expected


@pytest.mark.parametrize(
    ["name", "expected"],
    [
        ("env add", ["env remove", "env activate", "env info", "env list", "env use"]),
        ("evn add", ["env activate", "env use"]),
        ("env", ["env remove", "env info", "env list", "env use"]),
    ],
)
def test_find_similar_names(name: str, expected: list[str]) -> None:
    names = ["env info", "env use", "env activate", "env remove", "env list"]
    assert find_similar_names(name, names) == expected


@pytest.mark.parametrize(
    "value, expected", (("<ab> cde</>", " cde"), ("<ab", "<ab"), ("cd>", "cd>"))
)
def test_strip_tags(value: str, expected: str) -> None:
    assert strip_tags(value) == expected


@pytest.mark.parametrize(
    ("c", "expected"),
    [
        ("\0", 0),
        ("\n", -1),
        ("a", 1),
        ("1", 1),
        ("א", 1),
        ("\u200b", 0),
        ("\u1abe", 0),
        ("\u0591", 0),
        ("🉐", 2),
        ("＄", 2),  # noqa: RUF001
    ],
)
def test_wcwidth(c: str, expected: int) -> None:
    assert wcwidth(c) == expected


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("", 0),
        ("hello, world!", 13),
        ("hello, world!\n", -1),
        ("0123456789", 10),
        ("שלום, עולם!", 11),
        ("שְבֻעָיים", 6),
        ("🉐🉐🉐", 6),
    ],
)
def test_wcswidth(s: str, expected: int) -> None:
    assert wcswidth(s) == expected
