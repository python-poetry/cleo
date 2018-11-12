# -*- coding: utf-8 -*-

import os
import pytest

from cleo import Application, CommandTester
from cleo.exceptions.input import InvalidArgument

from .fixtures.hello_command import HelloCommand
from .fixtures.command_with_colons import CommandWithColons

app = Application()
app.add(HelloCommand())
app.add(CommandWithColons())


def test_invalid_shell():
    command = app.find("completions")
    tester = CommandTester(command)

    with pytest.raises(InvalidArgument):
        tester.execute([("shell", "pomodoro")])


def test_bash(mocker):
    mocker.patch(
        "cleo.commands.completions_command.CompletionsCommand._get_script_full_name",
        return_value="/path/to/my/script",
    )
    mocker.patch(
        "cleo.commands.completions_command.CompletionsCommand._generate_function_name",
        return_value="_my_function",
    )

    command = app.find("completions")
    tester = CommandTester(command)
    tester.execute([("shell", "bash")])

    output = tester.get_display()

    with open(os.path.join(os.path.dirname(__file__), "fixtures", "bash.txt")) as f:
        expected = f.read()

    assert expected == output


def test_zsh(mocker):
    mocker.patch(
        "cleo.commands.completions_command.CompletionsCommand._get_script_full_name",
        return_value="/path/to/my/script",
    )
    mocker.patch(
        "cleo.commands.completions_command.CompletionsCommand._generate_function_name",
        return_value="_my_function",
    )

    command = app.find("completions")
    tester = CommandTester(command)
    tester.execute([("shell", "zsh")])

    output = tester.get_display()

    with open(os.path.join(os.path.dirname(__file__), "fixtures", "zsh.txt")) as f:
        expected = f.read()

    assert expected == output


def test_fish(mocker):
    mocker.patch(
        "cleo.commands.completions_command.CompletionsCommand._get_script_full_name",
        return_value="/path/to/my/script",
    )
    mocker.patch(
        "cleo.commands.completions_command.CompletionsCommand._generate_function_name",
        return_value="_my_function",
    )

    command = app.find("completions")
    tester = CommandTester(command)
    tester.execute([("shell", "fish")])

    output = tester.get_display()

    with open(os.path.join(os.path.dirname(__file__), "fixtures", "fish.txt")) as f:
        expected = f.read()

    assert expected == output
