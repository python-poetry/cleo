from __future__ import annotations

import os
import sys

from io import StringIO
from typing import TYPE_CHECKING

import pytest

from cleo.io.buffered_io import BufferedIO
from cleo.io.inputs.string_input import StringInput


if TYPE_CHECKING:
    from typing import Iterator


@pytest.fixture()
def io() -> BufferedIO:
    input_ = StringInput("")
    input_.set_stream(StringIO())

    return BufferedIO(input_)


@pytest.fixture()
def ansi_io() -> BufferedIO:
    input_ = StringInput("")
    input_.set_stream(StringIO())

    return BufferedIO(input_, decorated=True)


@pytest.fixture()
def environ() -> Iterator[None]:
    current_environ = dict(os.environ)

    yield

    os.environ.clear()
    os.environ.update(current_environ)


@pytest.fixture()
def argv() -> Iterator[None]:
    current_argv = sys.argv

    yield

    sys.argv = current_argv
