# -*- coding: utf-8 -*-

from .command import Command
from ..helpers import DescriptorHelper


class ListCommand(Command):
    """
    Lists commands

    list {namespace? : The namespace name}
         {--raw : To output raw command list}
         {--format=txt : The output format (txt, json, or md)}
    """

    help = """The <info>%command.name%</info> command lists all commands:

  <info>python %command.full_name%</info>

You can also display the commands for a specific namespace:

  <info>python %command.full_name% test</info>

You can also output the information in other formats by using the <comment>--format</comment> option:

  <info>python %command.full_name% --format=json</info>

It's also possible to get raw list of commands (useful for embedding command runner):

  <info>python %command.full_name% --raw</info>"""

    def get_native_definition(self):
        return self.__class__().get_definition()

    def handle(self):
        helper = DescriptorHelper()
        helper.describe(
            self.output,
            self.get_application(),
            format=self.option('format'),
            raw_text=self.option('raw'),
            namespace=self.argument('namespace')
        )
