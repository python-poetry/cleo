from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar

from cleo.application import Application
from cleo.commands.command import Command
from cleo.helpers import argument
from cleo.testers.command_tester import CommandTester
from tests.fixtures.inherited_command import ChildCommand
from tests.fixtures.signature_command import SignatureCommand


if TYPE_CHECKING:
    from cleo.io.inputs.argument import Argument


class MyCommand(Command):
    name = "test"
    arguments: ClassVar[list[Argument]] = [
        argument("action", description="The action to execute.")
    ]

    def handle(self) -> int:
        action = self.argument("action")

        getattr(self, "_" + action)()
        return 0

    def _overwrite(self) -> None:
        self.write("Processing...")
        self.overwrite("Done!")


class MySecondCommand(Command):
    name = "test2"
    description = "Command testing"

    arguments: ClassVar[list[Argument]] = [argument("foo", "Bar", multiple=True)]

    def handle(self) -> int:
        foos = self.argument("foo")

        self.line(",".join(foos))
        return 0


def test_set_application() -> None:
    application = Application()
    command = Command()
    command.set_application(application)

    assert command.application == application


def test_with_signature() -> None:
    command = SignatureCommand()

    assert command.name == "signature:command"
    assert command.description == "description"
    assert command.help == "help"
    assert len(command.definition.arguments) == 2
    assert len(command.definition.options) == 2


def test_signature_inheritance() -> None:
    command = ChildCommand()

    assert command.name == "parent"
    assert command.description == "Parent Command."


def test_overwrite() -> None:
    command = MyCommand()

    tester = CommandTester(command)
    tester.execute("overwrite", decorated=True)

    expected = "Processing...\x1b[1G\x1b[2KDone!"
    assert tester.io.fetch_output() == expected


def test_explicit_multiple_argument() -> None:
    command = MySecondCommand()

    tester = CommandTester(command)
    tester.execute("1 2 3")

    assert tester.io.fetch_output() == "1,2,3\n"
