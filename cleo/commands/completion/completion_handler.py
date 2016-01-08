# -*- coding: utf-8 -*-

import os
import fnmatch
from ...inputs import ListInput
from .completion import Completion


class CompletionHandler(object):

    def __init__(self, application, context=None):
        self._application = application
        self._context = context
        self._helpers = []
        self._command = None

        self.add_handler(
            Completion(
                'help',
                'command_name',
                Completion.TYPE_ARGUMENT,
                list(application.all().keys())
            )
        )

        self.add_handler(
            Completion(
                'list',
                'namespace',
                Completion.TYPE_ARGUMENT,
                application.get_namespaces()
            )
        )

    def set_context(self, context):
        self._context = context

    def get_context(self):
        return self._context

    def add_handlers(self, handlers):
        self._helpers += handlers

    def add_handler(self, handler):
        self._helpers.append(handler)

    def run_completion(self):
        if not self._context:
            raise RuntimeError('A CompletionContext must be set before requesting completion.')

        cmd_name = self.get_input().get_first_argument()

        try:
            self._command = self._application.find(cmd_name)
        except Exception:
            # Exception raised, when multiple or none commands are found.
            pass

        process = [
            #'complete_for_option_values',
            'complete_for_option_shortcuts',
            #'complete_for_option_shortcut_values',
            'complete_for_options',
            'complete_for_command_name',
            'complete_for_command_arguments'
        ]

        for method in process:
            result = getattr(self, '_%s' % method)()

            if result is not False:
                # Return the result of the first completion mode that matches
                return self._filter_results(result)

        return []

    def get_input(self):
        """
        Get a ListInput representation of the completion context.

        :rtype: ListInput
        """
        # Filter the command line content to suit ListInput
        words = self._context.get_words()[:]
        if words:
            words.pop(0)

        words = list(filter(lambda x: x, words))

        return ListInput(words)

    def _complete_for_options(self):
        word = self._context.get_current_word()

        if word.startswith('-'):
            options = []

            for opt in self._get_all_options():
                options.append('--%s' % opt.get_name())

            return options

        return False

    def _complete_for_option_shortcuts(self):
        word = self._context.get_current_word()

        if word.startswith('-') and len(word) == 2:
            if self._command:
                definition = self._command.get_native_definition()
            else:
                definition = self._application.get_definition()

            if definition.has_shortcut(word[1]):
                return [word]

        return False

    def _complete_for_command_name(self):
        if (not self._command
            or (len(self._context.get_words()) == 2
                and self._context.get_word_index() == 1)):
            commands = self._application.all()
            names = list(commands.keys())

            key = names.index('_completion')
            del names[key]

            return names

        return False

    def _complete_for_command_arguments(self):
        """
        Attempt to complete the current word as a command argument value

        :rtype: list or False
        """
        if self._context.get_current_word().find('-') != 0 and self._command:
            arg_words = self._map_arguments_to_words(self._command.get_native_definition().get_arguments())
            word_index = self._context.get_word_index()

            if word_index in arg_words:
                name = arg_words[word_index]

                helper = self._get_completion_helper(name, Completion.TYPE_ARGUMENT)
                if helper:
                    return helper.run()

        return False

    def _get_completion_helper(self, name, type):
        """
        Find a Completion that matches the current command,
        target name, and target type

        :rtype: Completion
        """
        for helper in self._helpers:
            if helper.get_type() != type and helper.get_type() != Completion.ALL_TYPES:
                continue

            cmd = helper.get_command_name()
            if cmd == Completion.ALL_COMMANDS or cmd == self._command.get_name():
                if helper.get_target_name() == name:
                    return helper

        return

    def _map_arguments_to_words(self, arguments):
        argument_positions = {}
        argument_number = 0
        previous_word = None
        argument_names = [x.get_name() for x in arguments]

        # Build a list of option values to filter out
        option_with_args = self._get_option_words_with_values()

        for word_index, word in enumerate(self._context.get_words()):
            # Skip program name, command name, options, and option values
            if (word_index < 2
                or (word and '-' == word[0])
                or (previous_word in option_with_args)):
                previous_word = word
                continue

            previous_word = word

            # If argument n exists, pair that argument's name with the current word
            if argument_number < len(argument_names):
                argument_positions[word_index] = argument_names[argument_number]

            argument_number += 1

        return argument_positions

    def _get_option_words_with_values(self):
        """
        Step through the command line to determine which word positions represent which argument values

        The word indexes of argument values are found by eliminating words
        that are known to not be arguments (options, option values, and command names).
        Any word that doesn't match for elimination is assumed to be an argument value,

        :rtype: list
        """
        strings = []

        for option in self._get_all_options():
            if option.is_value_required():
                strings.append('--%s' % option.get_name())

                if option.get_shortcut():
                    strings.append('-%s' % option.get_shortcut())

        return strings

    def _get_all_options(self):
        """
        Get the combined options of the application and entered command.

        :rtype: list
        """
        application_options = self._application.get_definition().get_options()

        if not self._command:
            return application_options

        return [] + self._command.get_native_definition().get_options() + application_options

    def _filter_results(self, results):
        if not isinstance(results, list):
            results = [results]

        current_word = self._context.get_current_word()

        return list(filter(lambda x: fnmatch.fnmatch(x, '%s*' % current_word), results))

