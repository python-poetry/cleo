API Reference
#############

Command
=======

.. py:class:: Command(name=None)

    A ``Command`` represents a single CLI command.

    .. py:method:: argument(key=None)

        Get the value of a command argument.

        :param key: The argument name
        :type key: str

        :rtype: mixed

    .. py:method:: ask(question, default=None)

        Prompt the user for input.

        :param question: The question to ask
        :type question: str

        :param default: The default value
        :type default: str or None

        :rtype: str

    .. py:method:: call(name, options=None)

        Call another command.

        :param name: The command name
        :type name: str

        :param options: The options
        :type options: list or None

    .. py:method:: call_silent(name, options=None)

        Call another command silently.

        :param name: The command name
        :type name: str

        :param options: The options
        :type options: list or None

    .. py:method:: choice(question, choices, default=None, attempts=None, multiple=False)

        Give the user a single choice from an list of answers.

        :param question: The question to ask
        :type question: str

        :param choices: The available choices
        :type choices: list

        :param default: The default value
        :type default: str or None

        :param attempts: The max number of attempts
        :type attempts: int

        :param multiple: Multiselect
        :type multiple: int

        :rtype: str

    .. py:method:: comment(text)

        Write a string as comment output.

        :param text: The line to write
        :type text: str

    .. py:method:: confirm(self, question, default=False, true_answer_regex='(?i)^y')

        Confirm a question with the user.

        :param question: The question to ask
        :type question: str

        :param default: The default value
        :type default: bool

        :param true_answer_regex: A regex to match the "yes" answer
        :type true_answer_regex: str

        :rtype: bool

    .. py:method:: error(text)

        Write a string as error output.

        :param text: The line to write
        :type text: str

    .. py:method:: info(text)

        Write a string as information output.

        :param text: The line to write
        :type text: str

    .. py:method:: line(text, style=None, verbosity=None)

        Write a string as information output.

        :param text: The line to write
        :type text: str

        :param style: The style of the string
        :type style: str

        :param verbosity: The verbosity
        :type verbosity: None or int str

    .. py:method:: list(elements)

        Write a list of elements.

        :param elements: The elements to write a list for
        :type elements: list

    .. py:method:: option(key=None)

        Get the value of a command option.

        :param key: The option name
        :type key: str

        :rtype: mixed

    .. py:method:: progress_bar(max=0)

        Create a new progress bar

        :param max: The maximum number of steps
        :type max: int

        :rtype: ProgressBar

    .. py:method:: question(text)

        Write a string as question output.

        :param text: The line to write
        :type text: str

    .. py:method:: render_table(headers, rows, style='default')

        Format input to textual table..

        :param headers: The table headers
        :type headers: list

        :param rows: The table rows
        :type rows: list

        :param style: The table style
        :type style: str

    .. py:method:: secret(question)

        Prompt the user for input but hide the answer from the console.

        :param question: The question to ask
        :type question: str

        :rtype: str

    .. py:method:: set_style(name, fg=None, bg=None, options=None)

        Set a new style

        :param name: The name of the style
        :type name: str

        :param fg: The foreground color
        :type fg: str

        :param bg: The background color
        :type bg: str

        :param options: The options
        :type options: list

    .. py:method:: table(headers=None, rows=None, style='default')

        Return a ``Table`` instance.

        :param headers: The table headers
        :type headers: list

        :param rows: The table rows
        :type rows: list

        :param style: The table style
        :type style: str

    .. py:method:: table_cell(value, **options)

        Return a ``TableCell`` instance

        :param value: The cell value
        :type value: str

        :param options: The cell options
        :type options: dict

    .. py:method:: table_separator()

        Return a ``TableSeparator`` instance

        :rtype: TableSeparator

    .. py:method:: table_style()

        Return a ``TableStyle`` instance

        :rtype: TableStyle

    .. py:method:: warning(text)

        Write a string as warning output.

        :param text: The line to write
        :type text: str
