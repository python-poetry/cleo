import os
import sys

from io import StringIO

import pytest

from cleo.io.buffered_io import BufferedIO
from cleo.io.inputs.string_input import StringInput


@pytest.fixture()
def io():
    input_ = StringInput("")
    input_.set_stream(StringIO())

    return BufferedIO(input_)


@pytest.fixture()
def ansi_io():
    input_ = StringInput("")
    input_.set_stream(StringIO())

    return BufferedIO(input_, decorated=True)


@pytest.fixture()
def environ():
    current_environ = os.environ.copy()

    yield

    os.environ = current_environ


@pytest.fixture()
def argv():
    current_argv = sys.argv

    yield

    sys.argv = current_argv
