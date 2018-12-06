import os
import pytest

from cleo.commands import Command
from cleo.application import Application
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
    app.config.set_terminate_after_run(False)
    app.add(FooCommand())

    return app


@pytest.fixture()
def tester(app):
    return ApplicationTester(app)


def test_execute(tester):
    assert 0 == tester.execute("foo bar")
    assert 0 == tester.status_code
    assert "bar" + os.linesep == tester.io.fetch_output()
