# -*- coding: utf-8 -*-

from cleo import Command


class DescriptorCommand1(Command):
    """
    command 1 description

    descriptor:command1
    """

    aliases = ["alias1", "alias2"]

    help = "command 1 help"

    def _get_command_full_name(self):
        return "app/console " + self.name
