from __future__ import annotations

from cleo.helpers import tokenize
from cleo.io.inputs.argv_input import ArgvInput


class StringInput(ArgvInput):
    """
    Represents an input provided as a string
    """

    def __init__(self, input: str) -> None:
        super().__init__([])

        self._set_tokens(self._tokenize(input))

    def _tokenize(self, input: str) -> list[str]:
        return tokenize(input)
