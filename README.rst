Cleo
====

.. image:: https://travis-ci.org/SDisPater/cleo.svg?branch=master
    :target: https://travis-ci.org/SDisPater/cleo

Cleo allows you to create beautiful and testable command-line commands.

It is heavily inspired by the `Symfony Console Component <https://github.com/symfony/Console>`_,
with some useful additions.

Full documentation available here: http://cleo.readthedocs.org

Creating a basic Command
------------------------

To make a command that greets you from the command line,
create ``greet_command.py`` and add the following to it:

.. code-block:: python

    def greet(input_, output_):
        name = input_.get_argument('name')
        if name:
            text = 'Hello %s' % name
        else:
            text = 'Hello'

        if input_.get_option('yell'):
            text = text.upper()

        output_.writeln(text)

    greet_command = {
        'demo:greet': {
            'description': 'Greets someone',
            'arguments': [{
                'name': {
                    'description': 'Who do you want to greet?',
                    'required': False
                }
            }],
            'options': [{
                'yell': {
                    'shortcut': 'y',
                    'description': 'If set, the task will yell in uppercase letters',
                    'value_required': None
                }
            }],
            'code': greet
        }
    }

You also need to create the file to run at the command line which creates
an ``Application`` and adds commands to it:

.. code-block:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    from greet_command import greet_command
    from cleo import Application

    application = Application()
    application.add(greet_command)

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

.. note::

    The greet command can also be declared from a class called ``GreetCommand`` like so:

    .. code-block:: python

        from cleo import Command, InputArgument, InputOption


        class GreetCommand(Command):

            def configure():
                self.set_name('demo:greet')\
                    .set_description('Greets someone')\
                    .add_argument(
                        InputArgument('name',
                                      InputArgument.OPTIONAL,
                                      'Who do you want to greet?')
                    )\
                    .add_option(
                        InputOption('yell',
                                    'y',
                                    InputOption.VALUE_NONE,
                                    'If set, the task will yell in uppercase letters')
                    )

            def execute(input_, output_):
                name = input_.get_argument('name')
                if name:
                    text = 'Hello %s' % name
                else:
                    text = 'Hello'

                if input_.get_option('yell'):
                    text = text.upper()

                output_.writeln(text)

    Then you just have to import the ``GreetCommand`` class and add it to the application:

    .. code-block:: python

        application.add(GreetCommand())


Coloring the Output
~~~~~~~~~~~~~~~~~~~

Whenever you output text, you can surround the text with tags to color its
output. For example::

    # green text
    output_.writeln('<info>foo</info>')

    # yellow text
    output_.writeln('<comment>foo</comment>')

    # black text on a cyan background
    output_.writeln('<question>foo</question>')

    # white text on a red background
    output_.writeln('<error>foo</error>')

It is possible to define your own styles using the class ``OutputFormatterStyle``:

.. code-block:: python

    style = OutputFormatterStyle('red', 'yellow', ['bold', 'blink'])
    output_.get_formatter().set_style('fire', style)
    output_.writeln('<fire>foo</fire>')

Available foreground and background colors are: ``black``, ``red``, ``green``,
``yellow``, ``blue``, ``magenta``, ``cyan`` and ``white``.

And available options are: ``bold``, ``underscore``, ``blink``, ``reverse`` and ``conceal``.

You can also set these colors and options inside the tagname::

    # green text
    output_.writeln('<fg=green>foo</fg=green>')

    # black text on a cyan background
    output_.writeln('<fg=black;bg=cyan>foo</fg=black;bg=cyan>')

    # bold text on a yellow background
    output_.writeln('<bg=yellow;options=bold>foo</bg=yellow;options=bold>')

.. _verbosity-levels:

Verbosity Levels
~~~~~~~~~~~~~~~~

Cleo has 3 levels of verbosity. These are defined in the ``Output`` class:

=======================================  ==================================
Mode                                     Value
=======================================  ==================================
Output.VERBOSITY_QUIET                   Do not output any messages
Output.VERBOSITY_NORMAL                  The default verbosity level
Output.VERBOSITY_VERBOSE                 Increased verbosity of messages
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

    if Output.VERBOSITY_VERBOSE <= output_.get_verbosity():
        output_.writeln(...)

There are also more semantic methods you can use to test for each of the
verbosity levels:

.. code-block:: python

    if output_.is_quiet():
        # ...

    if output_.is_verbose():
        # ...

When the quiet level is used, all output is suppressed as the default
``Output.write()`` method returns without actually printing.
