from __future__ import annotations

from cleo.application import Application
from cleo.commands.command import Command
from cleo.helpers import argument
from cleo.testers.command_tester import CommandTester
from tests.fixtures.inherited_command import ChildCommand
from tests.fixtures.signature_command import SignatureCommand


class MyCommand(Command):
    """
    Command testing.

    test
        {action : The action to execute.}
    """

    def handle(self):
        action = self.argument("action")

        getattr(self, "_" + action)()

    def _overwrite(self):
        self.write("Processing...")
        self.overwrite("Done!")


class MySecondCommand(Command):

    name = "test2"
    description = "Command testing"

    arguments = [argument("foo", "Bar", multiple=True)]

    def handle(self):
        foos = self.argument("foo")

        self.line(",".join(foos))


class MyNamespacedCommand(Command):
    name = "test three"
    description = "Command testing"

    arguments = [argument("foo", "Bar", multiple=True)]

    def handle(self):
        foos = self.argument("foo")

        repeat = self.ask("Simon says:")
        self.line(",".join(foos))
        self.line(repeat)


def test_set_application():
    application = Application()
    command = Command()
    command.set_application(application)

    assert command.application == application


def test_with_signature():
    command = SignatureCommand()

    assert command.name == "signature:command"
    assert command.description == "description"
    assert command.help == "help"
    assert len(command.definition.arguments) == 2
    assert len(command.definition.options) == 2


def test_signature_inheritance():
    command = ChildCommand()

    assert command.name == "parent"
    assert command.description == "Parent Command."


def test_overwrite():
    command = MyCommand()

    tester = CommandTester(command)
    tester.execute("overwrite", decorated=True)

    expected = "Processing...\x1b[1G\x1b[2KDone!"
    assert tester.io.fetch_output() == expected


def test_explicit_multiple_argument():
    command = MySecondCommand()

    tester = CommandTester(command)
    tester.execute("1 2 3")

    assert tester.io.fetch_output() == "1,2,3\n"
