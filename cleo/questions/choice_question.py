# -*- coding: utf-8 -*-

import re
from .question import Question
from ..validators import Choice
from ..exceptions import CleoException
from .._compat import basestring, decode


class SelectChoiceValidator(Choice):

    def __init__(self, question, validator=None):
        """
        Constructor.

        :param question: A ChoiceQuestion instance
        :type question: ChoiceQuestion
        """
        super(SelectChoiceValidator, self).__init__(question.choices, validator)

        self.question = question

    def validate(self, selected):
        """
        Validate a choice.

        :param selected: The choice
        :type selected: str

        :return: bool
        """
        # Collapse all spaces.
        if not isinstance(selected, basestring):
            selected = decode(str(selected))

        selected_choices = selected.replace(' ', '')

        if self.question.multiselect:
            # Check for a separated comma values
            if not re.match('^[a-zA-Z0-9_-]+(?:,[a-zA-Z0-9_-]+)*$', selected_choices):
                raise CleoException(self.question.error_message % selected)

            selected_choices = selected_choices.split(',')
        else:
            selected_choices = [selected]

        multiselect_choices = []
        for value in selected_choices:
            results = []

            for key, choice in enumerate(self.values):
                if choice == value:
                    results.append(key)

            if len(results) > 1:
                raise CleoException(
                    'The provided answer is ambiguous. Value should be one of %s.'
                    % ' or '.join(results)
                )

            try:
                result = self.values.index(value)

                result = self.values[result]
            except ValueError:
                try:
                    value = int(value)

                    if value < len(self.values):
                        result = self.values[value]
                    else:
                        result = False
                except ValueError:
                    result = False

            if result is False:
                raise CleoException(self.question.error_message % value)

            multiselect_choices.append(result)

        if self.question.multiselect:
            return multiselect_choices

        return multiselect_choices[0]


class ChoiceQuestion(Question):
    """
    Represents a choice question.
    """

    multiselect = False
    prompt = ' > '
    error_message = 'Value "%s" is invalid'

    def __init__(self, question, choices, default=None):
        """
        Constructor.

        :param question: The question to ask to the user
        :type question: str

        :param choices: The list of available choices
        :type choices: list

        :param default: The default answer to return
        :type default: mixed
        """
        super(ChoiceQuestion, self).__init__(question, default)

        self.choices = choices
        self.validator = SelectChoiceValidator(self).validate
        self.autocompleter_values = choices
