# -*- coding: utf-8 -*-

from .command import Command
from ..inputs.input_argument import InputArgument
from ..inputs.input_option import InputOption
from ..inputs.input_definition import InputDefinition


class ListCommand(Command):

    def configure(self):
        self.set_name('list')\
            .set_definition(self.create_definition())\
            .set_description('Lists commands')\
            .set_help("""The <info>%command.name%</info> command lists all commands:

  <info>python %command.full_name%</info>

You can also display the commands for a specific namespace:

  <info>python %command.full_name% test</info>

It's also possible to get raw list of commands (useful for embedding command runner):

  <info>python %command.full_name% --raw</info>""")

    def get_native_definition(self):
        return self.create_definition()

    def execute(self, input_, output_):
        output_.write(
            self.get_application().as_text(
                input_.get_argument('namespace'),
                input_.get_option('raw'))
        )

    def create_definition(self):
        return InputDefinition([
            InputArgument('namespace', InputArgument.OPTIONAL, 'The namespace name', None),
            InputOption('raw', None, InputOption.VALUE_NONE, 'To output raw command list')
        ])
