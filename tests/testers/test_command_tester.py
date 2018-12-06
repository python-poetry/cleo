import os

import pytest

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


@pytest.fixture()
def tester():
    return CommandTester(FooCommand())


def test_execute(tester):
    assert 0 == tester.execute("bar")
    assert 0 == tester.status_code
    assert "bar" + os.linesep == tester.io.fetch_output()
