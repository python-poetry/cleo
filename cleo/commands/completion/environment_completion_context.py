# -*- coding: utf-8 -*-

import os
from .completion_context import CompletionContext


class EnvironmentCompletionContext(CompletionContext):

    def __init__(self):
        super(EnvironmentCompletionContext, self).__init__()

        self._command_line = os.getenv('CMDLINE_CONTENTS', False)
        self._char_index = int(os.getenv('CMDLINE_CURSOR_INDEX', 0))

        if self._command_line is False:
            raise RuntimeError('Failed to configure from environment; '
                               'Environment var CMDLINE_CONTENTS not set.')
