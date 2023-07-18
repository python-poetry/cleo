from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar

import pytest

from cleo.application import Application
from cleo.commands.command import Command
from cleo.helpers import argument
from cleo.testers.command_tester import CommandTester


if TYPE_CHECKING:
    from cleo.io.inputs.argument import Argument


class FooCommand(Command):
    name = "foo"
    description = "Foo command"
    arguments: ClassVar[list[Argument]] = [argument("foo", description="Foo argument")]

    def handle(self) -> int:
        self.line(self.argument("foo"))
        return 0


class FooBarCommand(Command):
    name = "foo bar"

    def handle(self) -> int:
        self.line("foo bar called")
        return 0


@pytest.fixture()
def tester() -> CommandTester:
    return CommandTester(FooCommand())


def test_execute(tester: CommandTester) -> None:
    assert tester.execute("bar") == 0
    assert tester.status_code == 0
    assert tester.io.fetch_output() == "bar\n"


def test_execute_namespace_command() -> None:
    app = Application()
    app.add(FooBarCommand())
    tester = CommandTester(app.find("foo bar"))

    assert tester.execute() == 0
    assert tester.status_code == 0
    assert tester.io.fetch_output() == "foo bar called\n"
