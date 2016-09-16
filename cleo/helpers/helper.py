# -*- coding: utf-8 -*-

from __future__ import division

import math
import re
from .._compat import decode


class Helper(object):

    helper_set = None

    time_formats = [
        (0, '< 1 sec'),
        (2, '1 sec'),
        (59, 'secs', 1),
        (60, '1 min'),
        (3600, 'mins', 60),
        (5400, '1 hr'),
        (86400, 'hrs', 3600),
        (129600, '1 day'),
        (604800, 'days', 86400),
    ]

    def set_helper_set(self, helper_set=None):
        """
        Sets the helper set associated with this helper.

        :param helper_set: A HelperSet instance
        :type helper_set: HelperSet
        """
        self.helper_set = helper_set

    def get_helper_set(self):
        """
        Gets the helper set associated with this helper.

        :return: A HelperSet instance
        :rtype: HelperSet
        """
        return self.helper_set

    @classmethod
    def len(cls, string):
        """
        Returns the length of a string.

        :param string: The string to return the length of
        :type string: str

        :return: The length of the string
        :rtype: int
        """
        return len(decode(string))

    @classmethod
    def format_time(cls, secs):
        """
        Format a duration in seconds to a human readable representation.

        :param secs: The duration in seconds
        :type secs: int

        :return: The duration representation
        :rtype: str
        """
        for fmt in cls.time_formats:
            if secs > fmt[0]:
                continue

            if len(fmt) == 2:
                return fmt[1]

            return '%s %s' % (int(math.ceil(secs / fmt[2])), fmt[1])

    @classmethod
    def format_memory(cls, memory):
        """
        Format a memory in bytes to a human readable representation.

        :param secs: The memory in bytes
        :type secs: int

        :return: The memory representation
        :rtype: str
        """
        if memory >= 1024**3:
            return '%.1f GiB' % (memory / 1024**3)

        if memory >= 1024 **2:
            return '%.1f MiB' % (memory / 1024**2)

        if memory >= 1024:
            return '%.1f KiB' % (memory / 1024)

        return '%.1f B' % memory

    @classmethod
    def len_without_decoration(cls, formatter, string):
        is_decorated = formatter.is_decorated()
        formatter.set_decorated(False)

        # Remove <...> formatting
        string = formatter.format(string)

        # Remove already formatted characters
        string = re.sub('\033\[[^m]*m', '', string)

        formatter.set_decorated(is_decorated)

        return cls.len(string)
