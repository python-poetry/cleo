from __future__ import annotations

import pytest

from cleo.commands.command import Command
from cleo.exceptions import CleoCommandNotFoundError
from cleo.loaders.factory_command_loader import FactoryCommandLoader


def command(name: str) -> Command:
    command_ = Command()
    command_.name = name

    return command_


def test_has() -> None:
    loader = FactoryCommandLoader(
        {"foo": lambda: command("foo"), "bar": lambda: command("bar")}
    )

    assert loader.has("foo")
    assert loader.has("bar")
    assert not loader.has("baz")


def test_get() -> None:
    loader = FactoryCommandLoader(
        {"foo": lambda: command("foo"), "bar": lambda: command("bar")}
    )

    assert isinstance(loader.get("foo"), Command)
    assert isinstance(loader.get("bar"), Command)


def test_get_invalid_command_raises_error() -> None:
    loader = FactoryCommandLoader(
        {"foo": lambda: command("foo"), "bar": lambda: command("bar")}
    )

    with pytest.raises(CleoCommandNotFoundError):
        loader.get("baz")


def test_names() -> None:
    loader = FactoryCommandLoader(
        {"foo": lambda: command("foo"), "bar": lambda: command("bar")}
    )

    assert loader.names == ["foo", "bar"]
