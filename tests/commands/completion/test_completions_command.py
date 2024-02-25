from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from cleo._compat import WINDOWS
from cleo.application import Application
from cleo.testers.command_tester import CommandTester
from tests.commands.completion.fixtures.command_with_colons import CommandWithColons
from tests.commands.completion.fixtures.command_with_space_in_name import SpacedCommand
from tests.commands.completion.fixtures.hello_command import HelloCommand


if TYPE_CHECKING:
    from pytest_mock import MockerFixture

FIXTURES_PATH = Path(__file__).parent / "fixtures"


app = Application()
app.add(HelloCommand())
app.add(CommandWithColons())
app.add(SpacedCommand())


def test_invalid_shell() -> None:
    command = app.find("completions")
    tester = CommandTester(command)

    with pytest.raises(ValueError):
        tester.execute("pomodoro")


@pytest.mark.skipif(WINDOWS, reason="Only test linux shells")
def test_bash(mocker: MockerFixture) -> None:
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

    with (FIXTURES_PATH / "bash.txt").open(encoding="utf-8") as f:
        expected = f.read()

    assert expected == tester.io.fetch_output().replace("\r\n", "\n")


@pytest.mark.skipif(WINDOWS, reason="Only test linux shells")
def test_zsh(mocker: MockerFixture) -> None:
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

    with (FIXTURES_PATH / "zsh.txt").open(encoding="utf-8") as f:
        expected = f.read()

    assert expected == tester.io.fetch_output().replace("\r\n", "\n")


@pytest.mark.skipif(WINDOWS, reason="Only test linux shells")
def test_fish(mocker: MockerFixture) -> None:
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

    with (FIXTURES_PATH / "fish.txt").open(encoding="utf-8") as f:
        expected = f.read()

    assert expected == tester.io.fetch_output().replace("\r\n", "\n")
