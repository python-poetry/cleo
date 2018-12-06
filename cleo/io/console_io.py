from clikit.io import ConsoleIO as BaseConsoleIO

from .io_mixin import IOMixin


class ConsoleIO(IOMixin, BaseConsoleIO):
    """
    A wrapper around CliKit's ConsoleIO.
    """

    def __init__(self, *args, **kwargs):
        super(ConsoleIO, self).__init__(*args, **kwargs)
