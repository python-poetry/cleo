from __future__ import annotations

from cleo.application import Application
from cleo.commands.list_command import ListCommand
from cleo.testers.command_tester import CommandTester


def test_version():
    command = ListCommand()
    command.set_application(Application("foo", "1.2.3"))

    tester = CommandTester(command)
    expected = "\x1b[39;1mFoo\x1b[39;22m (version \x1b[36m1.2.3\x1b[39m)\n"

    tester.execute("--version", decorated=True)
    assert expected == tester.io.fetch_output()

    tester.execute("-V", decorated=True)
    assert expected == tester.io.fetch_output()
