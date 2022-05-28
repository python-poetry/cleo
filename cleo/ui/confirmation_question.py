import re

from typing import Union

from cleo.io.io import IO

from .question import Question


class ConfirmationQuestion(Question):
    """
    Represents a yes/no question.
    """

    def __init__(
        self, question: str, default: bool = True, true_answer_regex: str = "(?i)^y"
    ) -> None:
        super().__init__(question, default)

        self._true_answer_regex = true_answer_regex
        self._normalizer = self._get_default_normalizer

    def _write_prompt(self, io: IO) -> None:
        message = self._question

        message = "<question>{} (yes/no)</> [<comment>{}</>] ".format(
            message, "yes" if self._default else "no"
        )

        io.write_error(message)

    def _get_default_normalizer(self, answer: Union[str, bool]) -> bool:
        """
        Default answer normalizer.
        """
        if isinstance(answer, bool):
            return answer

        answer_is_true = re.match(self._true_answer_regex, answer) is not None
        if self.default is False:
            return answer and answer_is_true

        return not answer or answer_is_true
