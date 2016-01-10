# -*- coding: utf-8 -*-


class CleoException(Exception):

    code = 1


class UsageError(CleoException):

    code = 2


class MissingArguments(UsageError):

    pass


class NoSuchOption(UsageError):

    pass


class TooManyArguments(UsageError):

    pass


class BadOptionUsage(UsageError):

    pass
