from __future__ import annotations

from io import StringIO
from typing import TYPE_CHECKING

from cleo.io.buffered_io import BufferedIO
from cleo.io.inputs.argv_input import ArgvInput
from cleo.io.inputs.string_input import StringInput


if TYPE_CHECKING:
    from cleo.commands.command import Command
    from cleo.io.outputs.output import Verbosity


class CommandTester:
    """
    Eases the testing of console commands.
    """

    def __init__(self, command: Command) -> None:
        self._command = command
        self._io = BufferedIO()
        self._inputs = []
        self._status_code = None

    @property
    def command(self) -> Command:
        return self._command

    @property
    def io(self) -> BufferedIO:
        return self._io

    @property
    def status_code(self) -> int:
        return self._status_code

    def execute(
        self,
        args: str | None = "",
        inputs: str | None = None,
        interactive: bool | None = None,
        verbosity: Verbosity | None = None,
        decorated: bool | None = None,
        supports_utf8: bool = True,
    ) -> int:
        """
        Executes the command
        """
        application = self._command.application

        input = StringInput(args)
        if application is not None and application.definition.has_argument("command"):
            name = self._command.name
            if " " in name:
                # If the command is namespaced we rearrange
                # the input to parse it as a single argument
                argv = [application.name, self._command.name] + input._tokens

                input = ArgvInput(argv)
            else:
                input = StringInput(name + " " + args)

        self._io.set_input(input)
        self._io.output.set_supports_utf8(supports_utf8)
        self._io.error_output.set_supports_utf8(supports_utf8)

        if inputs is not None:
            self._io.input.set_stream(StringIO(inputs))

        if interactive is not None:
            self._io.interactive(interactive)

        if verbosity is not None:
            self._io.set_verbosity(verbosity)

        if decorated is not None:
            self._io.decorated(decorated)

        self._status_code = self._command.run(self._io)

        return self._status_code
