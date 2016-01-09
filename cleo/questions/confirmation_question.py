# -*- coding: utf-8 -*-

import re
from .question import Question


class ConfirmationQuestion(Question):
    """
    Represents a yes/no question.
    """

    def __init__(self, question, default=True, true_answer_regex='(?i)^y'):
        """
        Constructor.

        :param question: The question to ask to the user
        :type question: str

        :param default: The default answer to return, True or False
        :type default: bool

        :param true_answer_regex: A regex to match the "yes" answer
        :type true_answer_regex: str
        """
        super(ConfirmationQuestion, self).__init__(question, default)

        self.true_answer_regex = true_answer_regex
        self.normalizer = self._get_default_normalizer

    def _get_default_normalizer(self, answer):
        """
        Default answer normalizer.
        """
        if isinstance(answer, bool):
            return answer

        answer_is_true = re.match(self.true_answer_regex, answer) is not None
        if self.default is False:
            return answer and answer_is_true

        return not answer or answer_is_true


