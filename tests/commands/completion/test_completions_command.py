from __future__ import annotations

import shutil
import subprocess

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
ZSH = shutil.which("zsh")


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

    expected = (FIXTURES_PATH / "bash.txt").read_text(encoding="utf-8")

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

    expected = (FIXTURES_PATH / "zsh.txt").read_text(encoding="utf-8")

    assert expected == tester.io.fetch_output().replace("\r\n", "\n")


@pytest.mark.skipif(WINDOWS, reason="Only test linux shells")
def test_zsh_handles_namespaced_commands(mocker: MockerFixture) -> None:
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
    script = tester.io.fetch_output().replace("\r\n", "\n")

    assert (
        '            ("spaced")\n            coms+=("command:Command with space in name.")'
        in script
    )
    assert '            ("spaced command")\n            opts+=("--goodbye")' in script

    if ZSH is None:
        return

    probe = (
        "setopt no_nomatch\n"
        "compdef(){ :; }\n"
        "_arguments(){ :; }\n"
        "_describe(){\n"
        "  local label=$1\n"
        "  local array_name=$2\n"
        "  local -a values\n"
        '  values=("${(@P)array_name}")\n'
        '  print -- "LABEL:$label"\n'
        "  print -rl -- $values\n"
        "}\n"
        "words=(script '')\n"
        "CURRENT=2\n"
        f"{script}\n"
        'print -- "--command-state--"\n'
        "words=(script spaced '')\n"
        "CURRENT=3\n"
        "_my_function\n"
        'print -- "--option-state--"\n'
        "words=(script spaced command --g)\n"
        "CURRENT=4\n"
        "_my_function\n"
    )
    result = subprocess.run(
        [ZSH, "-fc", probe],
        check=True,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )

    assert (
        "--command-state--\nLABEL:command\ncommand:Command with space in name.\n"
        in result.stdout
    )
    assert "--option-state--\nLABEL:option\n" in result.stdout
    assert result.stdout.rstrip().endswith("--goodbye")


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

    expected = (FIXTURES_PATH / "fish.txt").read_text(encoding="utf-8")

    assert expected == tester.io.fetch_output().replace("\r\n", "\n")
