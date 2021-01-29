import re

from typing import List

from .argv_input import ArgvInput
from .token_parser import TokenParser


class StringInput(ArgvInput):
    """
    Represents an input provided as a string
    """

    def __init__(self, input: str) -> None:
        super().__init__([])

        self._set_tokens(self._tokenize(input))

    def _tokenize(self, input: str) -> List[str]:
        return TokenParser().parse(input)
