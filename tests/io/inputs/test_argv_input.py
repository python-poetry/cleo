from __future__ import annotations

import sys

from typing import TYPE_CHECKING

import pytest

from cleo.io.inputs.argument import Argument
from cleo.io.inputs.argv_input import ArgvInput
from cleo.io.inputs.definition import Definition
from cleo.io.inputs.option import Option


if TYPE_CHECKING:
    from typing import Iterator


@pytest.fixture()
def argv() -> Iterator[None]:
    original = sys.argv[:]

    yield

    sys.argv = original


def test_it_uses_argv_by_default(argv: Iterator[None]) -> None:
    sys.argv = ["cli.py", "foo"]

    i = ArgvInput()

    assert ["foo"] == i._tokens


def test_parse_arguments() -> None:
    i = ArgvInput(["cli.py", "foo"])
    i.bind(Definition([Argument("name")]))

    assert i.arguments == {"name": "foo"}


@pytest.mark.parametrize(
    ["args", "options", "expected_options"],
    [
        (["cli.py", "--foo"], [Option("--foo")], {"foo": True}),
        (
            ["cli.py", "--foo=bar"],
            [Option("--foo", "-f", flag=False, requires_value=True)],
            {"foo": "bar"},
        ),
        (
            ["cli.py", "--foo", "bar"],
            [Option("--foo", "-f", flag=False, requires_value=True)],
            {"foo": "bar"},
        ),
        (
            ["cli.py", "--foo="],
            [Option("--foo", "-f", flag=False, requires_value=False)],
            {"foo": ""},
        ),
        (
            ["cli.py", "--foo=", "bar"],
            [Option("--foo", "-f", flag=False, requires_value=False), Argument("name")],
            {"foo": ""},
        ),
        (
            ["cli.py", "bar", "--foo="],
            [Option("--foo", "-f", flag=False, requires_value=False), Argument("name")],
            {"foo": ""},
        ),
        (
            ["cli.py", "--foo"],
            [Option("--foo", "-f", flag=False, requires_value=False)],
            {"foo": None},
        ),
        (
            ["cli.py", "-f"],
            [Option("--foo", "-f")],
            {"foo": True},
        ),
        (
            ["cli.py", "-fbar"],
            [Option("--foo", "-f", flag=False, requires_value=True)],
            {"foo": "bar"},
        ),
        (
            ["cli.py", "-f", "bar"],
            [Option("--foo", "-f", flag=False, requires_value=True)],
            {"foo": "bar"},
        ),
        (
            ["cli.py", "-f", ""],
            [Option("--foo", "-f", flag=False, requires_value=False)],
            {"foo": ""},
        ),
        (
            ["cli.py", "-f", "", "foo"],
            [Option("--foo", "-f", flag=False, requires_value=False), Argument("name")],
            {"foo": ""},
        ),
        (
            ["cli.py", "-f", "", "-b"],
            [
                Option("--foo", "-f", flag=False, requires_value=False),
                Option("--bar", "-b"),
            ],
            {"foo": "", "bar": True},
        ),
        (
            ["cli.py", "-f", "-b", "foo"],
            [
                Option("--foo", "-f", flag=False, requires_value=False),
                Option("--bar", "-b"),
                Argument("name"),
            ],
            {"foo": None, "bar": True},
        ),
        (
            ["cli.py", "-fb"],
            [
                Option("--foo", "-f"),
                Option("--bar", "-b"),
            ],
            {"foo": True, "bar": True},
        ),
        (
            ["cli.py", "-fb", "bar"],
            [
                Option("--foo", "-f"),
                Option("--bar", "-b", flag=False, requires_value=True),
            ],
            {"foo": True, "bar": "bar"},
        ),
        (
            ["cli.py", "-fbbar"],
            [
                Option("--foo", "-f", flag=False, requires_value=False),
                Option("--bar", "-b", flag=False, requires_value=False),
            ],
            {"foo": "bbar", "bar": None},
        ),
    ],
)
def test_parse_options(
    args: list[str],
    options: list[Option],
    expected_options: dict[str, str | bool | None],
) -> None:
    i = ArgvInput(args)
    i.bind(Definition(options))

    assert i.options == expected_options
