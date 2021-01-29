import pytest

from cleo.application import Application
from cleo.commands.command import Command
from cleo.testers.application_tester import ApplicationTester


class FooCommand(Command):
    """
    Foo command

    foo
        {foo : Foo argument}
    """

    def handle(self):
        self.line(self.argument("foo"))


@pytest.fixture()
def app():
    app = Application()
    app.add(FooCommand())

    return app


@pytest.fixture()
def tester(app):
    return ApplicationTester(app)


def test_execute(tester):
    assert 0 == tester.execute("foo bar")
    assert 0 == tester.status_code
    assert "bar\n" == tester.io.fetch_output()
