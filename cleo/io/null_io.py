from typing import Optional

from .inputs.input import Input
from .inputs.string_input import StringInput
from .io import IO
from .outputs.null_output import NullOutput


class NullIO(IO):
    def __init__(self, input: Optional[Input] = None) -> None:
        if input is None:
            input = StringInput("")

        super().__init__(input, NullOutput(), NullOutput())
