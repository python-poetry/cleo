# -*- coding: utf-8 -*-

from .exception import UsageException


class InvalidArgument(UsageException):

    pass


class InvalidOption(UsageException):

    pass


class MissingArguments(UsageException):

    pass


class NoSuchOption(UsageException):

    pass


class TooManyArguments(UsageException):

    pass


class BadOptionUsage(UsageException):

    pass
