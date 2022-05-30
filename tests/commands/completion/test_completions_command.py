from __future__ import annotations

import os

import pytest

from cleo.application import Application
from cleo.testers.command_tester import CommandTester
from tests.commands.completion.fixtures.command_with_colons import CommandWithColons
from tests.commands.completion.fixtures.hello_command import HelloCommand


app = Application()
app.add(HelloCommand())
app.add(CommandWithColons())


def test_invalid_shell():
    command = app.find("completions")
    tester = CommandTester(command)

    with pytest.raises(ValueError):
        tester.execute("pomodoro")


def test_bash(mocker):
    mocker.patch(
        "cleo.io.inputs.string_input.StringInput.script_name",
        new_callable=mocker.PropertyMock,
        return_value="/path/to/my/script",
    )
    mocker.patch(
        "cleo.commands.completions_command.CompletionsCommand._generate_function_name",
        return_value="_my_function",
    )

    command = app.find("completions")
    tester = CommandTester(command)
    tester.execute("bash")

    with open(os.path.join(os.path.dirname(__file__), "fixtures", "bash.txt")) as f:
        expected = f.read()

    assert expected == tester.io.fetch_output().replace("\r\n", "\n")


def test_zsh(mocker):
    mocker.patch(
        "cleo.io.inputs.string_input.StringInput.script_name",
        new_callable=mocker.PropertyMock,
        return_value="/path/to/my/script",
    )
    mocker.patch(
        "cleo.commands.completions_command.CompletionsCommand._generate_function_name",
        return_value="_my_function",
    )

    command = app.find("completions")
    tester = CommandTester(command)
    tester.execute("zsh")

    with open(os.path.join(os.path.dirname(__file__), "fixtures", "zsh.txt")) as f:
        expected = f.read()

    assert expected == tester.io.fetch_output().replace("\r\n", "\n")


def test_fish(mocker):
    mocker.patch(
        "cleo.io.inputs.string_input.StringInput.script_name",
        new_callable=mocker.PropertyMock,
        return_value="/path/to/my/script",
    )
    mocker.patch(
        "cleo.commands.completions_command.CompletionsCommand._generate_function_name",
        return_value="_my_function",
    )

    command = app.find("completions")
    tester = CommandTester(command)
    tester.execute("fish")

    with open(os.path.join(os.path.dirname(__file__), "fixtures", "fish.txt")) as f:
        expected = f.read()

    assert expected == tester.io.fetch_output().replace("\r\n", "\n")
