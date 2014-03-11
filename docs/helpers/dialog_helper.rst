Dialog Helper
=============

The ``DialogHelper`` class provides
functions to ask the user for more information. It is included in the default
helper set, which you can get by calling
``Command.get_helper_set()`` method:

.. code-block:: python

    dialog = self.get_helper_set().get('dialog')

All the methods inside the Dialog Helper have an
``Output`` instance as the first argument,
the question as the second argument and the default value as the last argument.

Asking the User for confirmation
--------------------------------

Suppose you want to confirm an action before actually executing it. Add
the following to your command:

.. code-block:: python

    # ...
    if dialog.ask_confirmation(
        output_,
        '<question>Continue with this action?</question>',
        False
    ):
        return

In this case, the user will be asked "Continue with this action?", and will
return ``True`` if the user answers with ``y`` or ``False`` if the user answers
with ``n``. The third argument to ``DialogHelper.ask_confirmation()`` method
is the default value to return if the user doesn't enter any input. Any other
input will ask the same question again.

Asking the User for Information
-------------------------------

You can also ask question with more than a simple yes/no answer. For instance,
if you want to know the user name, you can add this to your command:

.. code-block:: python

    # ...
    name = dialog.ask(
        output_,
        'Please enter your name',
        'John Doe'
    )

The user will be asked "Please enter your name". They can type
some name which will be returned by the
``DialogHelper.ask()`` method.
If they leave it empty, the default value (``John Doe`` here) is returned.

Autocompletion
~~~~~~~~~~~~~~

You can also specify an array of potential answers for a given question. These
will be autocompleted as the user types:

.. code-block:: python

    dialog = self.get_helper_set().get('dialog')
    roles = ['admin', 'manager', 'developer']
    role = dialog.ask(
        output_,
        'Please enter your role',
        'developer',
        roles
    )

Hiding the User's Response
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also ask a question and hide the response. This is particularly
convenient for passwords:

.. code-block:: python

    dialog = self.get_helper_set().get('dialog')
    password = dialog.ask_hidden_response(
        output_,
        'What is the database password?',
        False
    )

.. caution::

    When you ask for a hidden response, Cleo will use either a binary, change
    stty mode or use another trick to hide the response. If none is available,
    it will fallback and allow the response to be visible unless you pass ``False``
    as the third argument like in the example above. In this case, a RuntimeException
    would be thrown.

Validating the Answer
---------------------

You can even validate the answer. For instance, in the last example you asked
for the user name. A name should be composed of a first name and last name.
You can validate that by using the ``DialogHelper.ask_and_validate()``
method:

.. code-block:: python

    # ...
    def validate_answer(answer):
        if answer.split(' ') <= 1:
            raise Exception('The name should be include a first name and a last name')

        return answer

    bundle = dialog.ask_and_validate(
        output_,
        'Please enter the name of the bundle',
        validate_answer,
        False,
        'John Doe'
    )

This methods has 2 new arguments, the full signature is::

    ask_and_validate(
        Output output,
        str|list question,
        callable validator,
        int attempts = False,
        str default = None
    )

The ``validator`` is a callback which handles the validation. It should
raise an exception if there is something wrong. The exception message is displayed
in the console, so it is a good practice to put some useful information in it. The callback
function should also return the value of the user's input if the validation was successful.

You can set the max number of times to ask in the ``attempts`` argument.
If you reach this max number it will use the default value, which is given
in the last argument. Using ``False`` means the amount of attempts is infinite.
The user will be asked as long as they provide an invalid answer and will only
be able to proceed if their input is valid.

Validating a Hidden Response
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also ask and validate a hidden response:

.. code-block:: python

    dialog = self.get_helper_set().get('dialog')

    def validate(value):
        if value.strip() == '':
            raise Exception('The password can not be empty')

        return value

    password = dialog.ask_hidden_response_and_validate(
        output_,
        'Please enter your password',
        validate,
        20,
        False
    )

If you want to allow the response to be visible if it cannot be hidden for
some reason, pass true as the fifth argument.

Let the user choose from a list of Answers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have a predefined set of answers the user can choose from, you
could use the ``ask`` method described above or, to make sure the user
provided a correct answer, the ``ask_and_validate`` method. Both have
the disadvantage that you need to handle incorrect values yourself.

Instead, you can use the ``DialogHelper.select()`` method,
which makes sure that the user can only enter a valid string
from a predefined list:

.. code-block:: python

    dialog = self.get_helper_set().get('dialog')
    colors = ['red', 'blue', 'yellow']

    color = dialog.select(
        output_,
        'Please select your favorite color (default to red)',
        colors,
        0
    )
    output_.writeln('You have just selected: %s' % colors[color])

    # ... do something with the color

The option which should be selected by default is provided with the fourth
argument. The default is ``None``, which means that no option is the default one.

If the user enters an invalid string, an error message is shown and the user
is asked to provide the answer another time, until they enter a valid string
or the maximum attempts is reached (which you can define in the fifth
argument). The default value for the attempts is ``False``, which means infinite
attempts. You can define your own error message in the sixth argument.

Testing a Command which expects input
-------------------------------------

If you want to write a unit test for a command which expects some kind of input
from the command line, you need to overwrite the HelperSet used by the command:

.. code-block:: python

    from io import BytesIO
    from cleo import CommandTester

    # ...
    def test_execute()
    {
        # ...
        command_tester = CommandTester(command)

        dialog = command.get_helper('dialog')
        dialog.set_input_stream(self.get_input_stream('Test\n'))
        # Equals to a user inputing "Test" and hitting ENTER
        # If you need to enter a confirmation, "yes\n" will work

        command_tester.execute([('command', command.get_name())])

        # self.assertRegex('/.../', command_tester.get_display())
    }

    def get_input_stream(input_)
    {
        stream = BytesIO()
        stream.write(input_.encode())
        stream.seek(0)

        return stream
    }

By setting the input stream of the ``DialogHelper``, you imitate what the
console would do internally with all user input through the cli. This way
you can test any user interaction (even complex ones) by passing an appropriate
input stream.
