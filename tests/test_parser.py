from __future__ import annotations

from cleo.parser import Parser


def test_basic_parameter_parsing() -> None:
    results = Parser.parse("command:name")

    assert results["name"] == "command:name"

    results = Parser.parse("command:name {argument} {--option}")

    assert results["name"] == "command:name"
    assert results["arguments"][0].name == "argument"
    assert results["options"][0].name == "option"
    assert results["options"][0].is_flag()

    results = Parser.parse("command:name {argument*} {--option=}")

    assert results["name"] == "command:name"
    assert results["arguments"][0].name == "argument"
    assert results["arguments"][0].is_required()
    assert results["arguments"][0].is_list()
    assert results["options"][0].name == "option"
    assert results["options"][0].requires_value()

    results = Parser.parse("command:name {argument?*} {--option=*}")

    assert results["name"] == "command:name"
    assert results["arguments"][0].name == "argument"
    assert not results["arguments"][0].is_required()
    assert results["arguments"][0].is_list()
    assert results["options"][0].name == "option"
    assert results["options"][0].is_list()

    results = Parser.parse(
        "command:name {argument?* : The argument description.}"
        "    {--option=* : The option description.}"
    )

    assert results["name"] == "command:name"
    assert results["arguments"][0].name == "argument"
    assert results["arguments"][0].description == "The argument description."
    assert not results["arguments"][0].is_required()
    assert results["arguments"][0].is_list()
    assert results["options"][0].name == "option"
    assert results["options"][0].description == "The option description."
    assert results["options"][0].is_list()

    results = Parser.parse(
        "command:name "
        "{argument?* : The argument description.}    "
        "{--option=* : The option description.}"
    )

    assert results["name"] == "command:name"
    assert results["arguments"][0].name == "argument"
    assert results["arguments"][0].description == "The argument description."
    assert not results["arguments"][0].is_required()
    assert results["arguments"][0].is_list()
    assert results["options"][0].name == "option"
    assert results["options"][0].description == "The option description."
    assert results["options"][0].is_list()


def test_shortcut_name_parsing() -> None:
    results = Parser.parse("command:name {--o|option}")

    assert results["name"] == "command:name"
    assert results["options"][0].name == "option"
    assert results["options"][0].shortcut == "o"
    assert results["options"][0].is_flag()

    results = Parser.parse("command:name {--o|option=}")

    assert results["name"] == "command:name"
    assert results["options"][0].name == "option"
    assert results["options"][0].shortcut == "o"
    assert results["options"][0].requires_value()

    results = Parser.parse("command:name {--o|option=*}")

    assert results["name"] == "command:name"
    assert results["options"][0].name == "option"
    assert results["options"][0].shortcut == "o"
    assert results["options"][0].is_list()

    results = Parser.parse("command:name {--o|option=* : The option description.}")

    assert results["name"] == "command:name"
    assert results["options"][0].name == "option"
    assert results["options"][0].shortcut == "o"
    assert results["options"][0].description == "The option description."
    assert results["options"][0].is_list()

    results = Parser.parse("command:name " "{--o|option=* : The option description.}")

    assert results["name"] == "command:name"
    assert results["options"][0].name == "option"
    assert results["options"][0].shortcut == "o"
    assert results["options"][0].description == "The option description."
    assert results["options"][0].is_list()
