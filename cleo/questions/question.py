# -*- coding: utf-8 -*-

from ..exceptions import CleoException


class Question(object):
    """
    Represents a Question
    """

    def __init__(self, question, default=None):
        """
        Constructor.

        :param question: The question to ask the user
        :type question: str

        :param default: The default answer to return if the user enters nothing
        :type default: mixed
        """
        self.question = question
        self.default = default

        self._attempts = None
        self._hidden = False
        self.hidden_fallback = True
        self._autocompleter_values = None
        self.validator = None
        self.normalizer = None

    @property
    def hidden(self):
        return self._hidden

    @hidden.setter
    def hidden(self, value):
        if self.autocompleter_values:
            raise CleoException('A hidden question cannot use the autocompleter.')

        self._hidden = value

    @property
    def autocompleter_values(self):
        return self._autocompleter_values

    @autocompleter_values.setter
    def autocompleter_values(self, values):
        """
        Sets values for the autocompleter.

        :param values: The autocomplete values
        :type values: list or None
        """
        if values is not None and not isinstance(values, list):
            raise CleoException('Autocompleter values can be either a list or None.')

        if self.hidden:
            raise CleoException('A hidden question cannot use the autocompleter.')

        self._autocompleter_values = values

    @property
    def max_attempts(self):
        return self._attempts

    @max_attempts.setter
    def max_attempts(self, attempts):
        if attempts is not None and attempts < 1:
            raise CleoException('Maximum number of attempts must be a positive value.')

        self._attempts = attempts


