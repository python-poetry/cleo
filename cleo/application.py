from typing import Optional
from typing import Tuple

from clikit.console_application import ConsoleApplication

from .commands import BaseCommand
from .commands.completions_command import CompletionsCommand
from .config import ApplicationConfig


class Application(ConsoleApplication, object):
    """
    An Application is the container for a collection of commands.

    This class is optimized for a standard CLI environment.

    Usage:
    >>> app = Application('myapp', '1.0 (stable)')
    >>> app.add(HelpCommand())
    >>> app.run()
    """

    def __init__(
        self, name=None, version=None, complete=True, config=None
    ):  # type: (str, str, bool, Optional[ApplicationConfig]) -> None
        if config is None:
            config = ApplicationConfig(name, version)

        super(Application, self).__init__(config)

        if complete:
            self.add(CompletionsCommand())

    def add_commands(self, *commands):  # type: (Tuple[BaseCommand]) -> None
        for command in commands:
            self.add(command)

    def add(self, command):  # type: (BaseCommand) -> Application
        """
        Adds a command object.
        """
        self.add_command(command.config)
        command.set_application(self)

        return self

    def find(self, name):  # type: (str) -> BaseCommand
        names = name.split(" ")
        command = self.get_command(names[0])
        for name in names[1:]:
            command = command.get_sub_command(name)

        return command.config.handler
