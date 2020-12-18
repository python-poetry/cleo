from cleo.parser import Parser


def test_basic_parameter_parsing():
    results = Parser.parse("command:name")

    assert "command:name" == results["name"]

    results = Parser.parse("command:name {argument} {--option}")

    assert "command:name" == results["name"]
    assert "argument" == results["arguments"][0].name
    assert "option" == results["options"][0].name
    assert results["options"][0].is_flag()

    results = Parser.parse("command:name {argument*} {--option=}")

    assert "command:name" == results["name"]
    assert "argument" == results["arguments"][0].name
    assert results["arguments"][0].is_required()
    assert results["arguments"][0].is_list()
    assert "option" == results["options"][0].name
    assert results["options"][0].requires_value()

    results = Parser.parse("command:name {argument?*} {--option=*}")

    assert "command:name" == results["name"]
    assert "argument" == results["arguments"][0].name
    assert not results["arguments"][0].is_required()
    assert results["arguments"][0].is_list()
    assert "option" == results["options"][0].name
    assert results["options"][0].is_list()

    results = Parser.parse(
        "command:name {argument?* : The argument description.}    {--option=* : The option description.}"
    )

    assert "command:name" == results["name"]
    assert "argument" == results["arguments"][0].name
    assert "The argument description." == results["arguments"][0].description
    assert not results["arguments"][0].is_required()
    assert results["arguments"][0].is_list()
    assert "option" == results["options"][0].name
    assert "The option description." == results["options"][0].description
    assert results["options"][0].is_list()

    results = Parser.parse(
        "command:name "
        "{argument?* : The argument description.}    "
        "{--option=* : The option description.}"
    )

    assert "command:name" == results["name"]
    assert "argument" == results["arguments"][0].name
    assert "The argument description." == results["arguments"][0].description
    assert not results["arguments"][0].is_required()
    assert results["arguments"][0].is_list()
    assert "option" == results["options"][0].name
    assert "The option description." == results["options"][0].description
    assert results["options"][0].is_list()


def test_shortcut_name_parsing():
    results = Parser.parse("command:name {--o|option}")

    assert "command:name" == results["name"]
    assert "option" == results["options"][0].name
    assert "o" == results["options"][0].shortcut
    assert results["options"][0].is_flag()

    results = Parser.parse("command:name {--o|option=}")

    assert "command:name" == results["name"]
    assert "option" == results["options"][0].name
    assert "o" == results["options"][0].shortcut
    assert results["options"][0].requires_value()

    results = Parser.parse("command:name {--o|option=*}")

    assert "command:name" == results["name"]
    assert "option" == results["options"][0].name
    assert "o" == results["options"][0].shortcut
    assert results["options"][0].is_list()

    results = Parser.parse("command:name {--o|option=* : The option description.}")

    assert "command:name" == results["name"]
    assert "option" == results["options"][0].name
    assert "o" == results["options"][0].shortcut
    assert "The option description." == results["options"][0].description
    assert results["options"][0].is_list()

    results = Parser.parse("command:name " "{--o|option=* : The option description.}")

    assert "command:name" == results["name"]
    assert "option" == results["options"][0].name
    assert "o" == results["options"][0].shortcut
    assert "The option description." == results["options"][0].description
    assert results["options"][0].is_list()
