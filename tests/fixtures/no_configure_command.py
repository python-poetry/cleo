# -*- coding: utf-8 -*-

from cleo.commands.command import Command
from cleo.inputs import InputArgument, InputOption


class NoConfigureCommand(Command):

    name = 'no:configure'

    description = 'description'

    help = 'help'

    arguments = [
        InputArgument('foo'),
        {
            'name': 'bar'
        }
    ]

    options = [
        InputOption('baz', 'z'),
        {
            'name': 'bazz',
            'shortcut': 'Z'
        }
    ]

    def execute(self, input_, output_):
        output_.writeln('execute called')

    def interact(self, input_, output_):
        output_.writeln('interact called')
