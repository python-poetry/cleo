# -*- coding: utf-8 -*-

from cleo.commands.command import Command


class SignatureCommand(Command):

    name = 'no:configure'
    signature = 'signature:command {foo} {bar?} {--z/baz} {--Z/bazz}'

    description = 'description'

    help = 'help'

    def handle(self):
        self.output.line('handle called')
