from clikit.api.args.format import Argument
from clikit.api.args.format import Option

from cleo.parser import Parser


def test_basic_parameter_parsing():
    results = Parser.parse("command:name")

    assert "command:name" == results["name"]

    results = Parser.parse("command:name {argument} {--option}")

    assert "command:name" == results["name"]
    assert "argument" == results["arguments"][0].name
    assert "option" == results["options"][0].long_name
    assert Option.NO_VALUE == results["options"][0].flags

    results = Parser.parse("command:name {argument*} {--option=}")

    assert "command:name" == results["name"]
    assert "argument" == results["arguments"][0].name
    assert Argument.MULTI_VALUED | Argument.REQUIRED == results["arguments"][0].flags
    assert "option" == results["options"][0].long_name
    assert Option.REQUIRED_VALUE == results["options"][0].flags

    results = Parser.parse("command:name {argument?*} {--option=*}")

    assert "command:name" == results["name"]
    assert "argument" == results["arguments"][0].name
    assert Argument.MULTI_VALUED | Argument.OPTIONAL == results["arguments"][0].flags
    assert "option" == results["options"][0].long_name
    assert Option.MULTI_VALUED == results["options"][0].flags

    results = Parser.parse(
        "command:name {argument?* : The argument description.}    {--option=* : The option description.}"
    )

    assert "command:name" == results["name"]
    assert "argument" == results["arguments"][0].name
    assert "The argument description." == results["arguments"][0].description
    assert Argument.MULTI_VALUED | Argument.OPTIONAL == results["arguments"][0].flags
    assert "option" == results["options"][0].long_name
    assert "The option description." == results["options"][0].description
    assert Option.MULTI_VALUED == results["options"][0].flags

    results = Parser.parse(
        "command:name "
        "{argument?* : The argument description.}    "
        "{--option=* : The option description.}"
    )

    assert "command:name" == results["name"]
    assert "argument" == results["arguments"][0].name
    assert "The argument description." == results["arguments"][0].description
    assert Argument.MULTI_VALUED | Argument.OPTIONAL == results["arguments"][0].flags
    assert "option" == results["options"][0].long_name
    assert "The option description." == results["options"][0].description
    assert Option.MULTI_VALUED == results["options"][0].flags


def test_shortcut_name_parsing():
    results = Parser.parse("command:name {--o|option}")

    assert "command:name" == results["name"]
    assert "option" == results["options"][0].long_name
    assert "o" == results["options"][0].short_name
    assert Option.NO_VALUE == results["options"][0].flags

    results = Parser.parse("command:name {--o|option=}")

    assert "command:name" == results["name"]
    assert "option" == results["options"][0].long_name
    assert "o" == results["options"][0].short_name
    assert Option.REQUIRED_VALUE == results["options"][0].flags

    results = Parser.parse("command:name {--o|option=*}")

    assert "command:name" == results["name"]
    assert "option" == results["options"][0].long_name
    assert "o" == results["options"][0].short_name
    assert Option.MULTI_VALUED == results["options"][0].flags

    results = Parser.parse("command:name {--o|option=* : The option description.}")

    assert "command:name" == results["name"]
    assert "option" == results["options"][0].long_name
    assert "o" == results["options"][0].short_name
    assert "The option description." == results["options"][0].description
    assert Option.MULTI_VALUED == results["options"][0].flags

    results = Parser.parse("command:name " "{--o|option=* : The option description.}")

    assert "command:name" == results["name"]
    assert "option" == results["options"][0].long_name
    assert "o" == results["options"][0].short_name
    assert "The option description." == results["options"][0].description
    assert Option.MULTI_VALUED == results["options"][0].flags
