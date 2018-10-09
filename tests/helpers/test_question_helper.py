# -*- coding: utf-8 -*-

import os
import subprocess
from io import BytesIO, StringIO

from .. import CleoTestCase
from cleo.helpers.question_helper import QuestionHelper
from cleo.helpers.helper_set import HelperSet
from cleo.helpers.formatter_helper import FormatterHelper
from cleo.outputs.stream_output import StreamOutput
from cleo.inputs import Input
from cleo._compat import PY2
from cleo.questions import Question, ConfirmationQuestion, ChoiceQuestion
from cleo._compat import decode


class QuestionHelperTest(CleoTestCase):

    def test_ask_choice(self):
        question_helper = QuestionHelper()

        helper_set = HelperSet([FormatterHelper()])
        question_helper.set_helper_set(helper_set)

        heroes = ['Superman', 'Batman', 'Spiderman']

        question_helper.input_stream = self.get_input_stream('\n1\n  1  \nJohn\n1\nJohn\n1\n0,2\n 0 , 2  \n\n\n')

        question = ChoiceQuestion('What is your favorite superhero?', heroes, '2')
        question.max_attempts = 1
        # First answer is an empty answer, we're supposed to receive the default value
        self.assertEqual(
            'Spiderman',
            question_helper.ask(self.get_input(), self.get_output_stream(), question)
        )

        question = ChoiceQuestion('What is your favorite superhero?', heroes)
        question.max_attempts = 1
        self.assertEqual(
            'Batman',
            question_helper.ask(self.get_input(), self.get_output_stream(), question)
        )
        self.assertEqual(
            'Batman',
            question_helper.ask(self.get_input(), self.get_output_stream(), question)
        )

        question = ChoiceQuestion('What is your favorite superhero?', heroes)
        question.error_message = 'Input "%s" is not a superhero!'
        question.max_attempts = 2
        output = self.get_output_stream()
        self.assertEqual(
            'Batman',
            question_helper.ask(self.get_input(), output, question)
        )

        output.get_stream().seek(0)
        self.assertRegex(decode(output.get_stream().read()), 'Input "John" is not a superhero!')

        try:
            question = ChoiceQuestion('What is your favorite superhero?', heroes, '1')
            question.max_attempts = 1
            output = self.get_output_stream()
            question_helper.ask(self.get_input(), output, question)
            self.fail()
        except Exception as e:
            self.assertEqual('Value "John" is invalid', str(e))

        question = ChoiceQuestion('What is your favorite superhero?', heroes, None)
        question.max_attempts = 1
        question.multiselect = True

        self.assertEqual(
            ['Batman'],
            question_helper.ask(self.get_input(), self.get_output_stream(), question)
        )
        self.assertEqual(
            ['Superman', 'Spiderman'],
            question_helper.ask(self.get_input(), self.get_output_stream(), question)
        )
        self.assertEqual(
            ['Superman', 'Spiderman'],
            question_helper.ask(self.get_input(), self.get_output_stream(), question)
        )

        question = ChoiceQuestion('What is your favorite superhero?', heroes, '0,1')
        question.max_attempts = 1
        question.multiselect = True

        self.assertEqual(
            ['Superman', 'Batman'],
            question_helper.ask(self.get_input(), self.get_output_stream(), question)
        )

        question = ChoiceQuestion('What is your favorite superhero?', heroes, ' 0 , 1 ')
        question.max_attempts = 1
        question.multiselect = True

        self.assertEqual(
            ['Superman', 'Batman'],
            question_helper.ask(self.get_input(), self.get_output_stream(), question)
        )

    def test_ask_choice_one_option(self):
        question_helper = QuestionHelper()

        helper_set = HelperSet([FormatterHelper()])
        question_helper.set_helper_set(helper_set)

        heroes = ['Superman']

        question_helper.input_stream = self.get_input_stream('0\n')

        question = ChoiceQuestion('What is your favorite superhero?', heroes)
        question.max_attempts = 1
        self.assertEqual(
            'Superman',
            question_helper.ask(self.get_input(), self.get_output_stream(), question)
        )

    def test_ask(self):
        dialog = QuestionHelper()
        dialog.input_stream = self.get_string_input_stream('\n8AM\n')

        question = Question('What time is it?', '2PM')
        self.assertEqual(
            '2PM',
            dialog.ask(self.get_input(), self.get_output_stream(), question)
        )
        output = self.get_output_stream()
        self.assertEqual(
            '8AM',
            dialog.ask(self.get_input(), output, question)
        )

        output.get_stream().seek(0)
        self.assertEqual('What time is it?', decode(output.get_stream().read()))

    def test_ask_hidden_response(self):
        if not self.has_tty_available():
            self.skipTest('`stty` is required to test hidden response functionality')

        dialog = QuestionHelper()
        dialog.input_stream = self.get_string_input_stream('8AM\n')

        question = Question('What time is it?')
        question.hidden = True

        self.assertEqual(
            '8AM',
            dialog.ask(self.get_input(), self.get_output_stream(), question)
        )

    def test_ask_confirmation(self):
        data = [
            ('', True),
            ('', False, False),
            ('y', True),
            ('yes', True),
            ('n', False),
            ('no', False),
        ]

        for d in data:
            dialog = QuestionHelper()
            dialog.input_stream = self.get_input_stream(d[0] + '\n')
            default = d[2] if len(d) > 2 else True
            question = ConfirmationQuestion('Do you like French fries?', default)
            self.assertEqual(
                d[1],
                dialog.ask(self.get_input(), self.get_output_stream(), question)
            )

    def test_ask_confirmation_with_custom_true_answer(self):
        dialog = QuestionHelper()

        dialog.input_stream = self.get_input_stream('j\ny\n')
        question = ConfirmationQuestion('Do you like French fries?', False, '(?i)^(j|y)')
        self.assertTrue(dialog.ask(self.get_input(), self.get_output_stream(), question))
        question = ConfirmationQuestion('Do you like French fries?', False, '(?i)^(j|y)')
        self.assertTrue(dialog.ask(self.get_input(), self.get_output_stream(), question))

    def test_ask_and_validate(self):
        dialog = QuestionHelper()
        dialog.set_helper_set(HelperSet([FormatterHelper()]))

        error = 'This is not a color!'
        def validator(color):
            if color not in ['white', 'black']:
                raise Exception(error)

            return color

        question = Question('What color was the white horse of Henry IV?', 'white')
        question.validator = validator
        question.max_attempts = 2

        dialog.input_stream = self.get_input_stream('\nblack\n')
        self.assertEqual(
            'white',
            dialog.ask(self.get_input(), self.get_output_stream(), question)
        )
        self.assertEqual(
            'black',
            dialog.ask(self.get_input(), self.get_output_stream(), question)
        )

        dialog.input_stream = self.get_input_stream('green\nyellow\norange\n')
        try:
            dialog.ask(self.get_input(), self.get_output_stream(), question)
            self.fail()
        except Exception as e:
            self.assertEqual(error, str(e))

    def test_select_choice_from_simple_choice(self):
        possible_choices = [
            'My environment 1',
            'My environment 2',
            'My environment 3',
        ]

        data = [
            (0, 'My environment 1'),
            (1, 'My environment 2'),
            (2, 'My environment 3'),
            ('My environment 1', 'My environment 1'),
            ('My environment 2', 'My environment 2'),
            ('My environment 3', 'My environment 3'),
        ]

        for d in data:
            dialog = QuestionHelper()
            dialog.input_stream = self.get_input_stream(str(d[0]) + '\n')
            dialog.set_helper_set(HelperSet([FormatterHelper()]))

            question = ChoiceQuestion('Please select the environment to load', possible_choices)
            question.max_attempts = 1
            answer = dialog.ask(self.get_input(), self.get_output_stream(), question)

            self.assertEqual(d[1], answer)

    def test_no_interaction(self):
        dialog = QuestionHelper()
        question = Question('Do you have a job?', 'not yet')
        self.assertEqual(
            'not yet',
            dialog.ask(self.get_input(False), self.get_output_stream(), question)
        )

    def get_input_stream(self, input_):
        stream = BytesIO()
        stream.write(input_.encode())
        stream.seek(0)

        return stream

    def get_string_input_stream(self, input_):
        stream = StringIO()
        if PY2:
            stream.write(input_.decode())
        else:
            stream.write(input_)

        stream.seek(0)

        return stream

    def get_input(self, interactive=True):
        input = Input()
        input.is_interactive = self.mock().MagicMock(return_value=interactive)

        return input

    def get_output_stream(self):
        stream = BytesIO()

        return StreamOutput(stream)

    def has_tty_available(self):
        with open(os.devnull, 'w') as devnull:
            exit_code = subprocess.call(['stty', '2'], stdout=devnull, stderr=devnull)

        return exit_code == 0
