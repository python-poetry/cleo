from typing import Optional

from clikit.api.args import Args
from clikit.api.command import Command as CliKitCommand
from clikit.api.config.command_config import CommandConfig

from cleo.io import ConsoleIO


class CommandError(Exception):
    pass


class BaseCommand(object):

    name = None

    description = None

    help = None

    arguments = []
    options = []

    aliases = []

    enabled = True
    hidden = False

    commands = []

    def __init__(self):
        self._application = None

        self._config = CommandConfig(self.name)
        self._config.set_description(self.description)
        self._config.set_help(self.help)
        for argument in self.arguments:
            self._config._format_builder.add_argument(argument)

        for option in self.options:
            self._config._format_builder.add_option(option)

        for alias in self.aliases:
            self._config.add_alias(alias)

        if not self.enabled:
            self._config.disable()

        if self.hidden:
            self._config.hide()

        if self.commands:
            for command in self.commands:
                self.add_sub_command(command)

        self._config.set_handler(self)

    @property
    def config(self):  # type: () -> CommandConfig
        return self._config

    @property
    def application(self):
        return self._application

    def handle(
        self, args, io, command
    ):  # type: (Args, ConsoleIO, CliKitCommand) -> Optional[int]
        raise NotImplementedError()

    def set_application(self, application):
        self._application = application

        for command in self.commands:
            command.set_application(application)

    def add_sub_command(self, command):  # type: (BaseCommand) -> None
        self._config.add_sub_command_config(command.config)

        command.set_application(self.application)

    def default(self, default=True):  # type: (bool) -> BaseCommand
        self._config.default(default)

        return self

    def anonymous(self):  # type: () -> BaseCommand
        self._config.anonymous()

        return self
