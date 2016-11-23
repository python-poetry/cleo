# -*- coding: utf-8 -*-

import sys
import os
from .. import Command
from .hook_factory import HookFactory
from .environment_completion_context import EnvironmentCompletionContext
from .completion_handler import CompletionHandler


class CompletionCommand(Command):
    """
    BASH completion hook.

    _completion
        {--g|generate-hook : Generate BASH code that sets up completion for this application.}
        {--p|program= : Program name that should trigger completion.
                        <comment>(defaults to the absolute application path)</comment>}
        {--m|multiple : Generated hook can be used for multiple applications.}
        {--shell-type= : Set the shell type (zsh or bash).
                         Otherwise this is determined automatically.}
    """

    hidden = True

    def handle(self):
        handler = CompletionHandler(self.get_application())

        if self.option('generate-hook'):
            program = os.path.realpath(sys.argv[0])

            factory = HookFactory()
            alias = self.option('program')
            multiple = bool(self.option('multiple'))

            # When completing for multiple apps having absolute path
            # in the alias doesn't make sense.
            if not alias and multiple:
                alias = os.path.basename(program)

            hook = factory.generate_hook(
                self.option('shell-type') or self.get_shell_type(),
                program,
                alias,
                multiple
            )

            self.output.write(hook, True)
        else:
            handler.set_context(EnvironmentCompletionContext())
            self.output.write(self._run_completion(handler), True)

    def _run_completion(self, handler):
        self._configure_completion(handler)

        return handler.run_completion()

    def _configure_completion(self, handler):
        pass

    def get_shell_type(self):
        shell = os.getenv('SHELL')
        if not shell:
            raise RuntimeError(
                'Could not read SHELL environment variable. '
                'Please specify your shell type using the --shell-type option.'
            )

        return os.path.basename(shell)

    def get_native_definition(self):
        return self.__class__().get_definition()
