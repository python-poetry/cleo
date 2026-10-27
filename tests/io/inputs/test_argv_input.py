from __future__ import annotations

import sys

from typing import TYPE_CHECKING

import pytest

from cleo.io.inputs.argument import Argument
from cleo.io.inputs.argv_input import ArgvInput
from cleo.io.inputs.definition import Definition
from cleo.io.inputs.option import Option


if TYPE_CHECKING:
    from collections.abc import Iterator


@pytest.fixture()
def argv() -> Iterator[None]:
    original = sys.argv[:]

    yield

    sys.argv = original


def test_it_uses_argv_by_default(argv: Iterator[None]) -> None:
    sys.argv = ["cli.py", "foo"]

    i = ArgvInput()

    assert i._tokens == ["foo"]


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


@pytest.mark.parametrize("args", [[], ["--other=value"]])
@pytest.mark.parametrize("values", ["--name", ["--name", "-n"]])
@pytest.mark.parametrize("default", [False, 0, None, "fallback", object()])
def test_parameter_option_returns_default_when_missing(
    args: list[str], values: str | list[str], default: object
) -> None:
    i = ArgvInput(["cli.py", *args])

    assert i.parameter_option(values, default=default) is default


@pytest.mark.parametrize(
    ["args", "expected"],
    [
        (["--name", "alice"], "alice"),
        (["-n", "alice"], "alice"),
        (["--name"], None),
    ],
)
def test_parameter_option_preserves_present_values(
    args: list[str], expected: str | None
) -> None:
    i = ArgvInput(["cli.py", *args])

    assert i.parameter_option(["--name", "-n"], default="fallback") == expected


@pytest.mark.parametrize("only_params", [False, True])
def test_parameter_option_default_after_end_of_options(only_params: bool) -> None:
    i = ArgvInput(["cli.py", "--", "--name", "alice"])
    default = object()

    result = i.parameter_option("--name", default=default, only_params=only_params)

    if only_params:
        assert result is default
    else:
        assert result == "alice"


@pytest.mark.parametrize("args", [[], ["--other=value"]])
def test_parameter_option_default_is_false(args: list[str]) -> None:
    i = ArgvInput(["cli.py", *args])

    assert i.parameter_option("--name") is False
