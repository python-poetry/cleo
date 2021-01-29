from cleo.application import Application
from cleo.commands.command import Command
from cleo.helpers import argument
from cleo.testers.command_tester import CommandTester

from ..fixtures.inherited_command import ChildCommand
from ..fixtures.signature_command import SignatureCommand


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


def test_set_application():
    application = Application()
    command = Command()
    command.set_application(application)

    assert application == command.application


def test_with_signature():
    command = SignatureCommand()

    assert "signature:command" == command.name
    assert "description" == command.description
    assert "help" == command.help
    assert 2 == len(command.definition.arguments)
    assert 2 == len(command.definition.options)


def test_signature_inheritance():
    command = ChildCommand()

    assert "parent" == command.name
    assert "Parent Command." == command.description


def test_overwrite():
    command = MyCommand()

    tester = CommandTester(command)
    tester.execute("overwrite", decorated=True)

    expected = "Processing...\x1b[1G\x1b[2KDone!"
    assert expected == tester.io.fetch_output()


def test_explicit_multiple_argument():
    command = MySecondCommand()

    tester = CommandTester(command)
    tester.execute("1 2 3")

    assert "1,2,3\n" == tester.io.fetch_output()
