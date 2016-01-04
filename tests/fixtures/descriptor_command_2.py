# -*- coding: utf-8 -*-

from cleo import Command


class DescriptorCommand2(Command):
    """
    command 2 description

    descriptor:command2 {argument_name} {--o|option_name}
    """

    help = 'command 2 help'

    usages = ['-o|--option_name <argument_name>', '<argument_name>']

    def _get_command_full_name(self):
        return 'app/console ' + self.name
