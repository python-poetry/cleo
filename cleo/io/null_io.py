from __future__ import annotations

from cleo.io.inputs.input import Input
from cleo.io.inputs.string_input import StringInput
from cleo.io.io import IO
from cleo.io.outputs.null_output import NullOutput


class NullIO(IO):
    def __init__(self, input: Input | None = None) -> None:
        if input is None:
            input = StringInput("")

        super().__init__(input, NullOutput(), NullOutput())
