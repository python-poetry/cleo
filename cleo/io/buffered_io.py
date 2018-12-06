from clikit.io import BufferedIO as BaseBufferedIO

from .io_mixin import IOMixin


class BufferedIO(IOMixin, BaseBufferedIO):
    """
    An I/O that reads from and writes to a buffer.
    """

    def __init__(self, *args, **kwargs):
        super(BufferedIO, self).__init__(*args, **kwargs)
