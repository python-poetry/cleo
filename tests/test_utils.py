from __future__ import annotations

import pytest

from cleo._utils import find_similar_names
from cleo._utils import format_time
from cleo._utils import strip_tags


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
        ("", ["help", "foo1", "foo2", "bar1", "bar2", "foo bar1", "foo bar2"]),
        ("hellp", ["help"]),
        ("bar2", ["bar2", "bar1", "foo bar2"]),
        ("bar1", ["bar1", "bar2", "foo bar1"]),
        ("foo", ["foo1", "foo2", "foo bar1", "foo bar2"]),
    ],
)
def test_find_similar_names(name: str, expected: list[str]) -> None:
    names = ["help", "foo1", "foo2", "bar1", "bar2", "foo bar1", "foo bar2"]
    assert find_similar_names(name, names) == expected


@pytest.mark.parametrize(
    "value, expected", (("<ab> cde</>", " cde"), ("<ab", "<ab"), ("cd>", "cd>"))
)
def test_strip_tags(value: str, expected: str) -> None:
    assert strip_tags(value) == expected
