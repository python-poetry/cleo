# -*- coding: utf-8 -*-

from ... import CleoTestCase
from .fixtures.basic_command import BasicCommand
from .fixtures.basic_command2 import BasicCommand2
from cleo import Application
from cleo.commands.completion.completion_context import CompletionContext
from cleo.commands.completion.completion_handler import CompletionHandler

class CompletionHandlerTestCase(CleoTestCase):

    def setUp(self):
        self.application = Application(complete=True)

        self.application.add_commands([
            BasicCommand(),
            BasicCommand2()
        ])

    def create_handler(self, command_line, cursor_index=None):
        context = CompletionContext()

        context.set_command_line(command_line)
        if cursor_index is None:
            cursor_index = len(command_line)

        context.set_char_index(cursor_index)

        return CompletionHandler(self.application, context)

    def get_terms(self, handler_output):
        return handler_output

    #def test_complete_app_name(self):
    #    handler = self.create_handler('app')

    #    # It's not valid to complete the application name, so this should return nothing
    #    self.assertEqual(handler.run_completion(), [])

    def test_complete_command_name(self):
        handler = self.create_handler('app ')

        self.assertEqual(
            handler.run_completion(),
            ['help', 'list', 'wave', 'walk:through']
        )

    def test_complete_command_name_non_match(self):
        handler = self.create_handler('app br')

        self.assertEqual(
            handler.run_completion(),
            []
        )

    def test_complete_command_name_partial_two_matches(self):
        handler = self.create_handler('app wa')

        self.assertEqual(
            self.get_terms(handler.run_completion()),
            ['wave', 'walk:through']
        )

    def test_complete_command_name_partial_one_match(self):
        handler = self.create_handler('app wav')

        self.assertEqual(
            self.get_terms(handler.run_completion()),
            ['wave']
        )

    def test_complete_single_dash(self):
        handler = self.create_handler('app wave -')

        # Short options are not given as suggestions
        self.assertEqual(
            handler.run_completion(),
            []
        )

    def test_complete_option_shortcut(self):
        handler = self.create_handler('app wave -j')

        # If a valid option shortcut is completed on, the shortcut is returned so that completion can continue
        self.assertEqual(
            self.get_terms(handler.run_completion()),
            ['-j']
        )

    def test_complete_double_dash(self):
        handler = self.create_handler('app wave --')

        self.assertIn(
            '--vigorous',
            self.get_terms(handler.run_completion())
        )

        self.assertIn(
            '--jazz-hands',
            self.get_terms(handler.run_completion())
        )

    def test_complete_option_full(self):
        handler = self.create_handler('app wave --jazz')

        self.assertNotIn(
            '--vigorous',
            self.get_terms(handler.run_completion())
        )

        self.assertIn(
            '--jazz-hands',
            self.get_terms(handler.run_completion())
        )

    def test_complete_options_order(self):
        handler = self.create_handler('app wave bruce --vi')
        self.assertIn(
            '--vigorous',
            self.get_terms(handler.run_completion())
        )

        handler = self.create_handler('app wave --vi --jazz-hands bruce', 13)

        self.assertIn(
            '--vigorous',
            self.get_terms(handler.run_completion())
        )
