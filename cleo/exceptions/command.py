# -*- coding: utf-8 -*-

from .exception import CleoException


class CommandNotFound(CleoException):

    def __init__(self, name, alternatives=None, code=1):
        if alternatives is None:
            alternatives = []

        self._name = name
        self._alternatives = alternatives

        super(CommandNotFound, self).__init__(self.message, code=1)

    @property
    def message(self):
        message = 'Command "{}" is not defined.'.format(self._name)

        if self.alternatives:
            if len(self._alternatives) == 1:
                message += '\n\nDid you mean this?\n    '
            else:
                message += '\n\nDid you mean one of these?\n    '

            message += '\n    '.join(self._alternatives)

        return message

    @property
    def name(self):
        return self._name

    @property
    def alternatives(self):
        return self._alternatives


class NamespaceNotFound(CommandNotFound):

    @property
    def message(self):
        message = 'There are no commands defined in the "{}" namespace.'.format(self._name)

        if self.alternatives:
            if len(self._alternatives) == 1:
                message += '\n\nDid you mean this?\n    '
            else:
                message += '\n\nDid you mean one of these?\n    '

            message += '\n    '.join(self._alternatives)

        return message


class AmbiguousCommand(CommandNotFound):

    @property
    def message(self):
        message = '\nCommand "{}" is ambiguous ({}).'.format(
            self._name, self.get_abbreviation_suggestions()
        )

        return message

    def get_abbreviation_suggestions(self):
        """
        Returns abbreviated suggestions in string format.

        :rtype: str
        """
        rest = ''
        if len(self._alternatives) > 2:
            rest = ' and {} more'.format(len(self._alternatives) - 2)

        return '{}, {}{}'.format(
            self._alternatives[0], self._alternatives[1], rest
        )


class AmbiguousNamespace(AmbiguousCommand):
    
    @property
    def message(self):
        message = 'The namespace "{}" is ambiguous ({}).'.format(
            self._name, self.get_abbreviation_suggestions()
        )

        return message
