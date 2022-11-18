from __future__ import annotations

import pytest

from cleo.exceptions import CleoLogicError
from cleo.io.inputs.argument import Argument


def test_optional_non_list_argument() -> None:
    argument = Argument(
        "foo",
        required=False,
        is_list=False,
        description="Foo description",
        default="bar",
    )

    assert argument.name == "foo"
    assert not argument.is_required()
    assert not argument.is_list()
    assert argument.description == "Foo description"
    assert argument.default == "bar"


def test_required_non_list_argument() -> None:
    argument = Argument("foo", is_list=False, description="Foo description")

    assert argument.name == "foo"
    assert argument.is_required()
    assert not argument.is_list()
    assert argument.description == "Foo description"
    assert argument.default is None


def test_list_argument() -> None:
    argument = Argument("foo", is_list=True, description="Foo description")

    assert argument.name == "foo"
    assert argument.is_required()
    assert argument.is_list()
    assert argument.description == "Foo description"
    assert argument.default == []


def test_required_arguments_do_not_support_default_values() -> None:
    with pytest.raises(
        CleoLogicError, match="Cannot set a default value for required arguments"
    ):
        Argument("foo", description="Foo description", default="bar")


def test_list_arguments_do_not_support_non_list_default_values() -> None:
    with pytest.raises(
        CleoLogicError, match="A default value for a list argument must be a list"
    ):
        Argument(
            "foo",
            required=False,
            is_list=True,
            description="Foo description",
            default="bar",
        )
