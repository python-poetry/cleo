from clikit.args import StringArgs

from cleo import Application
from cleo.io import BufferedIO


class ApplicationTester(object):
    """
    Eases the testing of console applications.
    """

    def __init__(self, application):  # type: (Application) -> None
        self._application = application
        self._application.config.set_terminate_after_run(False)
        self._io = BufferedIO()
        self._status_code = 0

    @property
    def io(self):  # type: () -> BufferedIO
        return self._io

    @property
    def status_code(self):  # type: () -> int
        return self._status_code

    def execute(self, args, **options):  # type: (str, ...) -> int
        """
        Executes the command

        Available options:
            * interactive: Sets the input interactive flag
            * verbosity: Sets the output verbosity flag
        """
        args = StringArgs(args)

        if "inputs" in options:
            self._io.set_input(options["inputs"])

        if "interactive" in options:
            self._io.set_interactive(options["interactive"])

        if "verbosity" in options:
            self._io.set_verbosity(options["verbosity"])

        self._status_code = self._application.run(
            args,
            self._io.input.stream,
            self._io.output.stream,
            self._io.error_output.stream,
        )

        return self._status_code
