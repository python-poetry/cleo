import pytest

from cleo.application import Application
from cleo.commands.command import Command
from cleo.testers.command_tester import CommandTester


class FooCommand(Command):
    """
    Foo command

    foo
        {foo : Foo argument}
    """

    def handle(self):
        self.line(self.argument("foo"))


class FooBarCommand(Command):

    name = "foo bar"

    def handle(self):
        self.line("foo bar called")


@pytest.fixture()
def tester():
    return CommandTester(FooCommand())


def test_execute(tester):
    assert tester.execute("bar") == 0
    assert tester.status_code == 0
    assert tester.io.fetch_output() == "bar\n"


def test_execute_namespace_command():
    app = Application()
    app.add(FooBarCommand())
    tester = CommandTester(app.find("foo bar"))

    assert tester.execute() == 0
    assert tester.status_code == 0
    assert tester.io.fetch_output() == "foo bar called\n"
