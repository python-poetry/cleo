# -*- coding: utf-8 -*-

from cleo.commands.command import Command
from cleo.validators import Integer, Boolean


class SignatureCommand(Command):

    name = "no:configure"
    signature = "signature:command {foo} {bar?} {--z|baz} {--Z|bazz}"

    description = "description"

    help = "help"

    validation = {"foo": Integer(), "--baz": Boolean()}

    def handle(self):
        self.output.line("handle called")
