import pytest

from cleo.application import Application
from cleo.commands.command import Command
from cleo.helpers import argument
from cleo.helpers import option
from cleo.testers.application_tester import ApplicationTester


class FooCommand(Command):
    """
    Foo command
    """

    name = "foo"

    description = "Foo command"

    arguments = [argument("foo")]

    options = [option("--bar")]

    def handle(self):
        self.line(self.argument("foo"))

        if self.option("bar"):
            self.line("--bar activated")


class FooBarCommand(Command):
    """
    Foo Bar command
    """

    name = "foo bar"

    description = "Foo Bar command"

    arguments = [argument("foo")]

    options = [option("--baz")]

    def handle(self):
        self.line(self.argument("foo"))

        if self.option("baz"):
            self.line("--baz activated")


@pytest.fixture()
def app():
    app = Application()
    app.add(FooCommand())
    app.add(FooBarCommand())

    return app


@pytest.fixture()
def tester(app):
    return ApplicationTester(app)


def test_execute(tester: ApplicationTester):
    assert 0 == tester.execute("foo baz --bar")
    assert 0 == tester.status_code
    assert "baz\n--bar activated\n" == tester.io.fetch_output()


def test_execute_namespace_command(tester: ApplicationTester):
    tester.application.catch_exceptions(False)
    assert 0 == tester.execute("foo bar baz --baz")
    assert 0 == tester.status_code
    assert "baz\n--baz activated\n" == tester.io.fetch_output()
