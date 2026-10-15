from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar

from cleo.application import Application
from cleo.commands.command import Command
from cleo.helpers import argument
from cleo.testers.application_tester import ApplicationTester
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


class CalleeCommand(Command):
    name = "callee"
    arguments: ClassVar[list[Argument]] = [argument("value", "The value to print.")]

    def handle(self) -> int:
        self.line(self.argument("value"))
        return 0


class CallerCommand(Command):
    name = "caller"

    def handle(self) -> int:
        return self.call("callee", "hello")


class SilentCallerCommand(Command):
    name = "silent-caller"

    def handle(self) -> int:
        return self.call_silent("callee", "hello")


def _app_with_callee_and(caller: Command) -> Application:
    application = Application()
    application.add(CalleeCommand())
    application.add(caller)

    return application


def test_call_binds_arguments_to_the_called_command() -> None:
    # Regression test for https://github.com/python-poetry/cleo/issues/130: the
    # application's own top-level "command" argument used to be first in line for
    # binding, so the called command's first real argument was silently swallowed
    # by that phantom slot instead of reaching the called command's own argument.
    tester = ApplicationTester(_app_with_callee_and(CallerCommand()))

    assert tester.execute("caller") == 0
    assert tester.io.fetch_output() == "hello\n"


def test_call_silent_binds_arguments_to_the_called_command() -> None:
    tester = ApplicationTester(_app_with_callee_and(SilentCallerCommand()))

    assert tester.execute("silent-caller") == 0
    # call_silent runs the called command against a NullIO, so its own output
    # isn't captured here -- the point of this test is that the call above didn't
    # raise "Not enough arguments" and returned a successful status code.
