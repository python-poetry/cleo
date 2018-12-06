Question Helper
###############
Asking the User for Confirmation
================================

Suppose you want to confirm an action before actually executing it. Add the following to your command:

.. code-block:: python

    def handle(self):
        if not self.confirm('Continue with this action?', False):
            return

In this case, the user will be asked "Continue with this action?".
If the user answers with ``y`` it returns ``True`` or ``False`` if they answer with ``n``.
The second argument to ``confirm()`` is the default value to return if the user doesn't enter any valid input.
If the second argument is not provided, ``True`` is assumed.

.. tip::

    You can customize the regex used to check if the answer means "yes" in the third argument of the ``customize()`` method.
    For instance, to allow anything that starts with either ``y`` or ``j``, you would set it to:

    .. code-block:: python

        self.confirm('Continue with this action?', False, '(?i)^(y|j)')

    The regex defaults to ``(?i)^y``.


Asking the User for Information
===============================

You can also ask a question with more than a simple yes/no answer.
For instance, if you want to know a user name, you can add this to your command:

.. code-block:: python

    def handle(self):
        name = self.ask('Please enter your name', 'John Doe')

The user will be asked "Please enter your name".
They can type some name which will be returned by the ``ask()`` method.
If they leave it empty, the default value (``John Doe`` here) is returned.

Let the User Choose from a List of Answers
------------------------------------------

If you have a predefined set of answers the user can choose from,
you could use a ``ChoiceQuestion`` or the ``choice()`` method which
makes sure that the user can only enter a valid string from a predefined list:

.. code-block:: python

    def handle(self):
        color = self.choice(
            'Please select your favorite color (defaults to red)',
            ['red', 'blue', 'yellow'],
            0
        )

        self.line('You have just selected: %s' % color)

The option which should be selected by default is provided with the third argument.
The default is ``None``, which means that no option is the default one.

If the user enters an invalid string, an error message is shown
and the user is asked to provide the answer another time,
until they enter a valid string or reach the maximum number of attempts.
The default value for the maximum number of attempts is ``None``, which means infinite number of attempts.

Multiple Choices
----------------

Sometimes, multiple answers can be given. The ``ChoiceQuestion`` or ``choice()`` method
provides this feature using comma separated values.
This is disabled by default, to enable this use the ``multiple`` keyword if using the ``choice()`` method
or the ``multiselect`` attribute if using the ``ChoiceQuestion`` directly:

.. code-block:: python

    def handle(self):
        colors = self.choice(
            'Please select your favorite color (defaults to red and blue),
            ['red', 'blue', 'yellow'],
            '0,1'
            multiple=True
        )

        self.line('You have just selected: %s' % ', '.join(colors))

Now, when the user enters ``1,2``, the result will be: ``You have just selected: blue, yellow``.

If the user does not enter anything, the result will be: ``You have just selected: red, blue``.

Autocompletion
--------------

You can also specify an array of potential answers for a given question.
These will be autocompleted as the user types:

.. code-block:: python

    def handle(self):
        names = ['John', 'Jane', 'Paul']
        question = self.create_question('Please enter a name', default='John')
        question.set_autocomplete_values(names)

        name = self.ask(question)

Hiding the User's Response
--------------------------

You can also ask a question and hide the response.
This is particularly convenient for passwords:

.. code-block:: python

    def handle(self):
        password = self.secret('What is the database password?')


Validating the Answer
=====================

You can even validate the answer.
For instance, you might only accept integers:

.. code-block:: python

    def handle(self):
        question = self.create_question('Choose a number')
        question.set_validator(int)
        question.set_max_attempts(2)

        number = self.ask(question)

The ``validator`` a callback which handles the validation.
It should throw an exception if there is something wrong.
The exception message is displayed in the console, so it is a good practice to put some useful information in it.
The validator or the callback function should also return the value of the user's input if the validation was successful.

You can set the max number of times to ask with the ``set_max_attempts()`` method.
If you reach this max number it will use the default value.
Using ``None`` means the amount of attempts is infinite.
The user will be asked as long as they provide an invalid answer
and will only be able to proceed if their input is valid.


Testing a Command that Expects Input
====================================

If you want to write a unit test for a command which expects some kind of input from the command line,
you need to set the helper input stream:

.. code-block:: python

    def test_execute_command(self):
        command_tester = CommandTester(command)
        # Equals to a user inputting "Test" and hitting ENTER
        # If you need to enter a confirmation, "yes\n" will work

        command_tester.execute(inputs="Test\n")
