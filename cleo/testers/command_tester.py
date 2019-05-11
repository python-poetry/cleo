from clikit.api.command import Command
from clikit.args import StringArgs
from clikit.formatter import AnsiFormatter

from cleo.commands import BaseCommand
from cleo.io import BufferedIO


class CommandTester(object):
    """
    Eases the testing of console commands.
    """

    def __init__(self, command):  # type: (BaseCommand) -> None
        """
        Constructor
        """
        self._command = command
        self._io = BufferedIO()
        self._inputs = []
        self._status_code = None

        if self._command.application:
            for style in self._command.application.config.style_set.styles.values():
                self._io.output.formatter.add_style(style)
                self._io.error_output.formatter.add_style(style)

    @property
    def io(self):  # type: () -> BufferedIO
        return self._io

    @property
    def status_code(self):  # type: () -> int
        return self._status_code

    def execute(self, args="", **options):  # type: (str, ...) -> int
        """
        Executes the command

        Available options:
            * interactive: Sets the input interactive flag
            * decorated: Sets the output decorated flag
            * verbosity: Sets the output verbosity flag
        """
        args = StringArgs(args)

        if "inputs" in options:
            self._io.set_input(options["inputs"])

        if "interactive" in options:
            self._io.set_interactive(options["interactive"])

        if "verbosity" in options:
            self._io.set_verbosity(options["verbosity"])

        if "decorated" in options and options["decorated"]:
            self._io.set_formatter(AnsiFormatter(forced=True))

        command = Command(self._command.config, self._command.application)

        self._status_code = command.run(args, self._io)

        return self._status_code
