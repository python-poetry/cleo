from clikit.api.args.format import Argument
from clikit.api.args.format import Option

from cleo import argument
from cleo import option


def test_argument():
    arg = argument("foo", "Foo")

    assert "Foo" == arg.description
    assert arg.is_required()
    assert not arg.is_optional()
    assert not arg.is_multi_valued()
    assert arg.default is None

    arg = argument("foo", "Foo", optional=True, default="bar")

    assert not arg.is_required()
    assert arg.is_optional()
    assert not arg.is_multi_valued()
    assert "bar" == arg.default

    arg = argument("foo", "Foo", multiple=True)

    assert arg.is_required()
    assert not arg.is_optional()
    assert arg.is_multi_valued()
    assert [] == arg.default

    arg = argument("foo", "Foo", optional=True, multiple=True, default=["bar"])

    assert not arg.is_required()
    assert arg.is_optional()
    assert arg.is_multi_valued()
    assert ["bar"] == arg.default


def test_option():
    opt = option("foo", "f", "Foo")

    assert "Foo" == opt.description
    assert not opt.accepts_value()
    assert not opt.is_value_optional()
    assert not opt.is_value_required()
    assert not opt.is_multi_valued()
    assert opt.default is None

    opt = option("foo", "f", "Foo", flag=False)

    assert "Foo" == opt.description
    assert opt.accepts_value()
    assert not opt.is_value_optional()
    assert opt.is_value_required()
    assert not opt.is_multi_valued()

    opt = option("foo", "f", "Foo", flag=False, value_required=False)

    assert "Foo" == opt.description
    assert opt.accepts_value()
    assert opt.is_value_optional()
    assert not opt.is_value_required()
    assert not opt.is_multi_valued()

    opt = option("foo", "f", "Foo", flag=False, multiple=True)

    assert "Foo" == opt.description
    assert opt.accepts_value()
    assert not opt.is_value_optional()
    assert opt.is_value_required()
    assert opt.is_multi_valued()
    assert [] == opt.default

    opt = option("foo", "f", "Foo", flag=False, default="bar")

    assert "Foo" == opt.description
    assert opt.accepts_value()
    assert not opt.is_value_optional()
    assert opt.is_value_required()
    assert not opt.is_multi_valued()
    assert "bar" == opt.default
