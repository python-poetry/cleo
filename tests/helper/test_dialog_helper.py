# -*- coding: utf-8 -*-

from io import BytesIO
import re

from unittest import TestCase
from cleo.helper.dialog_helper import DialogHelper
from cleo.helper.helper_set import HelperSet
from cleo.helper.formatter_helper import FormatterHelper
from cleo.output.stream_output import StreamOutput


class DialogHelperTest(TestCase):

    def test_select(self):
        """
        DialogHelper.select() behaves properly
        """
        dialog = DialogHelper()

        helper_set = HelperSet([FormatterHelper()])
        dialog.set_helper_set(helper_set)

        heroes = ['Superman', 'Batman', 'Spiderman']

        dialog.set_input_stream(self.get_input_stream('\n1\nSebastien\n1\nSebastien\nSebastien\n'))
        self.assertEqual('2',
                         dialog.select(self.get_output_stream(),
                                       'What is your favorite superhero?', heroes, '2'))
        self.assertEqual('1',
                         dialog.select(self.get_output_stream(),
                                       'What is your favorite superhero?', heroes).decode())

        output = self.get_output_stream()
        self.assertEqual('1',
                         dialog.select(output,
                                       'What is your favorite superhero?', heroes, None,
                                       False, 'Input "%s" is not a superhero!').decode())

        output.get_stream().seek(0)
        self.assertTrue(re.match('.*Input "Sebastien" is not a superhero!.*',
                                 output.get_stream().read().decode()) is not None)

        output = self.get_output_stream()
        self.assertRaises(Exception, dialog.select, output, 'What is your favorite superhero?', heroes, None, 1)

    def test_ask(self):
        """
        DialogHelper.ask() behaves properly
        """
        dialog = DialogHelper()
        dialog.set_input_stream(self.get_input_stream('\n8AM\n'))

        self.assertEqual('2PM', dialog.ask(self.get_output_stream(), 'What time is it?', '2PM'))
        output = self.get_output_stream()
        self.assertEqual('8AM', dialog.ask(output, 'What time is it?', '2PM').decode())

        output.get_stream().seek(0)
        self.assertEqual('What time is it?', output.get_stream().read().decode())

    def test_ask_confirmation(self):
        """
        DialogHelper.ask_confirmation() behaves properly
        """
        dialog = DialogHelper()

        dialog.set_input_stream(self.get_input_stream('\n\n'))
        self.assertTrue(dialog.ask_confirmation(self.get_output_stream(), 'Do you like French fries?'))
        self.assertFalse(dialog.ask_confirmation(self.get_output_stream(), 'Do you like French fries?', False))

        dialog.set_input_stream(self.get_input_stream('y\nyes\n'))
        self.assertTrue(dialog.ask_confirmation(self.get_output_stream(), 'Do you like French fries?', False))
        self.assertTrue(dialog.ask_confirmation(self.get_output_stream(), 'Do you like French fries?', False))

        dialog.set_input_stream(self.get_input_stream('n\nno\n'))
        self.assertFalse(dialog.ask_confirmation(self.get_output_stream(), 'Do you like French fries?', True))
        self.assertFalse(dialog.ask_confirmation(self.get_output_stream(), 'Do you like French fries?', True))

    def test_ask_and_validate(self):
        """
        DialogHelper.ask_and_validate() behaves properly
        """
        dialog = DialogHelper()
        helper_set = HelperSet([FormatterHelper()])
        dialog.set_helper_set(helper_set)

        question = 'What color was the white horse of Henry IV?'
        error = 'This is not a color!'

        def validator(color):
            if color not in ['white', 'black']:
                raise Exception(error)

            return color

        dialog.set_input_stream(self.get_input_stream('\nblack\n'))
        self.assertEqual('white', dialog.ask_and_validate(self.get_output_stream(), question, validator, 2, 'white'))
        self.assertEqual('black', dialog.ask_and_validate(self.get_output_stream(), question, validator, 2, 'white'))

        dialog.set_input_stream(self.get_input_stream('green\nyellow\norange\n'))
        self.assertRaises(Exception,
                          dialog.ask_and_validate,
                          self.get_output_stream(), question, validator, 2, 'white')

    def get_input_stream(self, input_):
        stream = BytesIO()
        stream.write(input_.encode())
        stream.seek(0)

        return stream

    def get_output_stream(self):
        stream = BytesIO()

        return StreamOutput(stream)
