Creating a basic Command
------------------------

Using classes
~~~~~~~~~~~~~

To make a command that greets you from the command line,
create ``greet_command.py`` and add the following to it:

.. code-block:: python

    from cleo import Command, InputArgument, InputOption


    class GreetCommand(Command):

        name = 'demo:greet'

        description = 'Greets someone'

        arguments = [
            {
                'name': 'name',
                'description': 'Who do you want to greet?',
                'required': False
            }
        ]

        options = [
            {
                'name': 'yell',
                'shortcut': 'y',
                'flag': True,
                'description': 'If set, the task will yell in uppercase letters'
            }
        ]

        def execute(i, o):
            """
            Executes the command.
    
            :type i: cleo.inputs.input.Input
            :type o: cleo.outputs.output.Output
            """
            name = i.get_argument('name')
            if name:
                text = 'Hello %s' % name
            else:
                text = 'Hello'

            if i.get_option('yell'):
                text = text.upper()

            o.writeln(text)
            

You also need to create the file to run at the command line which creates
an ``Application`` and adds commands to it:

.. code-block:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    from greet_command import GreetCommand
    from cleo import Application

    application = Application()
    application.add(GreetCommand())

    if __name__ == '__main__':
        application.run()

Test the new command by running the following

.. code-block:: bash

    $ python application.py demo:greet John

This will print the following to the command line:

.. code-block:: text

    Hello John

You can also use the ``--yell`` option to make everything uppercase:

.. code-block:: bash

    $ python application.py demo:greet John --yell

This prints:

.. code-block:: text

    HELLO JOHN

Using decorators
~~~~~~~~~~~~~~~~

.. versionadded:: 0.3

To register a new command you can also use provided decorators:

.. code-block:: python

    from cleo import Application
    
    app = Application()
    
    @app.command('demo:greet', description='Greets someone')
    @app.argument('name', description='Who do you want to greet?', required=False)
    @app.option('yell', description='If set, the task will yell in uppercase letters',
                flag=True)
    def greet(i, o):
        name = i.get_argument('name')
        if name:
            text = 'Hello %s' % name
        else:
            text = 'Hello'
    
        if i.get_option('yell'):
            text = text.upper()
    
        o.writeln(text)


Using dictionaries
~~~~~~~~~~~~~~~~~~

The greet command can also be declared with a dictionary like so:

.. code-block:: python
    
    from cleo import Application

    app = Application()


    def greet(i, o):
        name = i.get_argument('name')
        if name:
            text = 'Hello %s' % name
        else:
            text = 'Hello'

        if i.get_option('yell'):
            text = text.upper()

        o.writeln(text)

    greet_command = {
        'name': 'demo:greet',
        'description': 'Greets someone',
        'arguments': [{
            'name': 'name',
            'description': 'Who do you want to greet?',
            'required': False
        }],
        'options': [{
            'name': 'yell',
            'shortcut': 'y',
            'description': 'If set, the task will yell in uppercase letters',
            'flag': True
        }],
        'code': greet
    }

    app.add(greet_command)


.. _output-coloring:

Coloring the Output
~~~~~~~~~~~~~~~~~~~

Whenever you output text, you can surround the text with tags to color its
output. For example::

    # green text
    o.writeln('<info>foo</info>')

    # yellow text
    o.writeln('<comment>foo</comment>')

    # black text on a cyan background
    o.writeln('<question>foo</question>')

    # white text on a red background
    o.writeln('<error>foo</error>')

It is possible to define your own styles using the class ``OutputFormatterStyle``:

.. code-block:: python

    style = OutputFormatterStyle('red', 'yellow', ['bold', 'blink'])
    o.get_formatter().set_style('fire', style)
    o.writeln('<fire>foo</fire>')

Available foreground and background colors are: ``black``, ``red``, ``green``,
``yellow``, ``blue``, ``magenta``, ``cyan`` and ``white``.

And available options are: ``bold``, ``underscore``, ``blink``, ``reverse`` and ``conceal``.

You can also set these colors and options inside the tagname::

    # green text
    o.writeln('<fg=green>foo</fg=green>')

    # black text on a cyan background
    o.writeln('<fg=black;bg=cyan>foo</fg=black;bg=cyan>')

    # bold text on a yellow background
    o.writeln('<bg=yellow;options=bold>foo</bg=yellow;options=bold>')

.. _verbosity-levels:

Verbosity Levels
~~~~~~~~~~~~~~~~

Cleo has 3 levels of verbosity. These are defined in the ``Output`` class:

=======================================  ==================================
Mode                                     Value
=======================================  ==================================
``Output.VERBOSITY_QUIET``               Do not output any messages
``Output.VERBOSITY_NORMAL``              The default verbosity level
``Output.VERBOSITY_VERBOSE``             Increased verbosity of messages
=======================================  ==================================

You can specify the quiet verbosity level with the ``--quiet`` or ``-q``
option. The ``--verbose`` or ``-v`` option is used when you want an increased
level of verbosity.

.. tip::

    The full exception stacktrace is printed if the ``VERBOSITY_VERBOSE``
    level or above is used.

It is possible to print a message in a command for only a specific verbosity
level. For example:

.. code-block:: python

    if Output.VERBOSITY_VERBOSE <= o.get_verbosity():
        o.writeln(...)

There are also more semantic methods you can use to test for each of the
verbosity levels:

.. code-block:: python

    if o.is_quiet():
        # ...

    if o.is_verbose():
        # ...

When the quiet level is used, all output is suppressed as the default
``Output.write()`` method returns without actually printing.


Autocompletion
~~~~~~~~~~~~~~

.. versionadded:: 0.3

Cleo now supports autocompletion of commands.
However it is not completely automatic. First you have to use the ``bash_completion.sh`` file:

.. code-block:: bash

    # In your .bashrc or .zshrc
    source /path/to/bash_completion.sh

Now, if your script is named ``console`` autocompletion is set. If not add a line like the following:

.. code-block:: bash

    complete -F _complete_console you-script-name
