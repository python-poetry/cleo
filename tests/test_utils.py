from __future__ import annotations

import pytest

from cleo._utils import find_similar_names


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
def test_find_similar_names(name: str, expected: list[str]):
    names = ["help", "foo1", "foo2", "bar1", "bar2", "foo bar1", "foo bar2"]
    assert find_similar_names(name, names) == expected
