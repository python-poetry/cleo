from __future__ import annotations

from cleo.helpers import argument
from cleo.helpers import option


def test_argument() -> None:
    arg = argument("foo", "Foo")

    assert arg.description == "Foo"
    assert arg.is_required()
    assert not arg.is_list()
    assert arg.default is None

    arg = argument("foo", "Foo", optional=True, default="bar")

    assert not arg.is_required()
    assert not arg.is_list()
    assert arg.default == "bar"

    arg = argument("foo", "Foo", multiple=True)

    assert arg.is_required()
    assert arg.is_list()
    assert [] == arg.default

    arg = argument("foo", "Foo", optional=True, multiple=True, default=["bar"])

    assert not arg.is_required()
    assert arg.is_list()
    assert ["bar"] == arg.default


def test_option() -> None:
    opt = option("foo", "f", "Foo")

    assert opt.description == "Foo"
    assert not opt.accepts_value()
    assert not opt.requires_value()
    assert not opt.is_list()
    assert opt.default is False

    opt = option("foo", "f", "Foo", flag=False)

    assert opt.description == "Foo"
    assert opt.accepts_value()
    assert opt.requires_value()
    assert not opt.is_list()
    assert opt.default is None

    opt = option("foo", "f", "Foo", flag=False, value_required=False)

    assert opt.description == "Foo"
    assert opt.accepts_value()
    assert not opt.requires_value()
    assert not opt.is_list()

    opt = option("foo", "f", "Foo", flag=False, multiple=True)

    assert opt.description == "Foo"
    assert opt.accepts_value()
    assert opt.requires_value()
    assert opt.is_list()
    assert opt.default == []

    opt = option("foo", "f", "Foo", flag=False, default="bar")

    assert opt.description == "Foo"
    assert opt.accepts_value()
    assert opt.requires_value()
    assert not opt.is_list()
    assert opt.default == "bar"
