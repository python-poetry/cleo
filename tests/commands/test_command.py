# -*- coding: utf-8 -*-
from cleo.application import Application
from cleo.commands.command import Command
from cleo.testers import CommandTester

from ..fixtures.signature_command import SignatureCommand
from ..fixtures.inherited_command import ChildCommand


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


def test_set_application():
    application = Application()
    command = Command()
    command.set_application(application)

    assert application == command.application


def test_with_signature():
    command = SignatureCommand()
    config = command.config

    assert "signature:command" == config.name
    assert "description" == config.description
    assert "help" == config.help
    assert 2 == len(config.arguments)
    assert 2 == len(config.options)


def test_signature_inheritance():
    command = ChildCommand()
    config = command.config

    assert "parent" == config.name
    assert "Parent Command." == config.description


def test_overwrite():
    command = MyCommand()

    tester = CommandTester(command)
    tester.execute("overwrite", decorated=True)
    print(repr(tester.io.fetch_output()))

    expected = "Processing...{}Done!        {}".format("\x08" * 13, "\x08" * 8)
    assert expected == tester.io.fetch_output()
