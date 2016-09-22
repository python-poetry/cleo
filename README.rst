Cleo
####

.. image:: https://travis-ci.org/sdispater/cleo.png
   :alt: Cleo Build status
   :target: https://travis-ci.org/sdispater/cleo

Create beautiful and testable command-line interfaces.

Resources
=========

* `Documentation <http://cleo.readthedocs.io>`_
* `Issue Tracker <https://github.com/sdispater/cleo/issues>`_


Usage
=====

To make a command that greets you from the command line,
create ``greet_command.py`` and add the following to it:

.. code-block:: python

    from cleo import Command


    class GreetCommand(Command):
        """
        Greets someone

        demo:greet
            {name? : Who do you want to greet?}
            {--y|yell : If set, the task will yell in uppercase letters}
        """

        def handle(self):
            name = self.argument('name')

            if name:
                text = 'Hello %s' % name
            else:
                text = 'Hello'

            if self.option('yell'):
                text = text.upper()

            self.line(text)


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

As you may have already seen, Cleo uses the command docstring to determine
the command definition.
The docstring must be in the following form :

.. code-block:: python

    """
    Command description

    Command signature
    """

The signature being in the following form:

.. code-block:: python

    """
    command:name {argument : Argument description} {--option : Option description}
    """

The signature can span multiple lines.

.. code-block:: python

    """
    command:name
        {argument : Argument description}
        {--option : Option description}
    """

Coloring the Output
-------------------

Whenever you output text, you can surround the text with tags to color its
output. For example:

.. code-block:: python

    # green text
    self.line('<info>foo</info>')

    # yellow text
    self.line('<comment>foo</comment>')

    # black text on a cyan background
    self.line('<question>foo</question>')

    # white text on a red background
    self.line('<error>foo</error>')

The closing tag can be replaced by ``</>``, which revokes all formatting options established by the last opened tag.

You can also use the corresponding methods:

.. code-block:: python

    self.info('foo')
    self.comment('foo')
    self.question('foo')
    self.error('foo')

It is possible to define your own styles using the ``set_style()`` method:

.. code-block:: python

    self.set_style('fire', fg='red', bg='yellow', options=['bold', 'blink'])
    self.line('<fire>foo</fire>')

Available foreground and background colors are: ``black``, ``red``, ``green``,
``yellow``, ``blue``, ``magenta``, ``cyan`` and ``white``.

And available options are: ``bold``, ``underscore``, ``blink``, ``reverse`` and ``conceal``.

You can also set these colors and options inside the tagname:

.. code-block:: python

    # green text
    self.line('<fg=green>foo</>')

    # black text on a cyan background
    self.line('<fg=black;bg=cyan>foo</>')

    # bold text on a yellow background
    self.line('<bg=yellow;options=bold>foo</>')


Verbosity Levels
----------------

Cleo has five verbosity levels. These are defined in the ``Output`` class:

=======================================  ================================== ======================
Mode                                     Meaning                            Console option
=======================================  ================================== ======================
``Output.VERBOSITY_QUIET``               Do not output any messages         ``-q`` or ``--quiet``
``Output.VERBOSITY_NORMAL``              The default verbosity level        (none)
``Output.VERBOSITY_VERBOSE``             Increased verbosity of messages    ``-v``
``Output.VERBOSITY_VERY_VERBOSE``        Informative non essential messages ``-vv``
``Output.VERBOSITY_DEBUG``               Debug messages                     ``-vvv``
=======================================  ================================== ======================

It is possible to print a message in a command for only a specific verbosity
level. For example:

.. code-block:: python

    if Output.VERBOSITY_VERBOSE <= self.output.get_verbosity():
        self.line(...)

There are also more semantic methods you can use to test for each of the
verbosity levels:

.. code-block:: python

    if self.output.is_quiet():
        # ...

    if self.output.is_verbose():
        # ...

When the quiet level is used, all output is suppressed as the default
``Output.write()`` method returns without actually printing.


Using Arguments
---------------

The most interesting part of the commands are the arguments and options that
you can make available. Arguments are the strings - separated by spaces - that
come after the command name itself. They are ordered, and can be optional
or required. For example, add an optional ``last_name`` argument to the command
and make the ``name`` argument required:

.. code-block:: python

    class GreetCommand(Command):
        """
        Greets someone

        demo:greet
            {name : Who do you want to greet?}
            {last_name? : Your last name?}
            {--y|yell : If set, the task will yell in uppercase letters}
        """

You now have access to a ``last_name`` argument in your command:

.. code-block:: python

    last_name = self.argument('last_name')
    if last_name:
        text += ' %s' % last_name

The command can now be used in either of the following ways:

.. code-block:: bash

    $ python application.py demo:greet John
    $ python application.py demo:greet John Doe

It is also possible to let an argument take a list of values (imagine you want
to greet all your friends). For this it must be specified at the end of the
argument list:

.. code-block:: python

    class GreetCommand(Command):
        """
        Greets someone

        demo:greet
            {names* : Who do you want to greet?}
            {--y|yell : If set, the task will yell in uppercase letters}
        """

To use this, just specify as many names as you want:

.. code-block:: bash

    $ python application.py demo:greet John Jane

You can access the ``names`` argument as a list:

.. code-block:: python

    names = self.argument('names')
    if names:
        text += ' %s' % ', '.join(names)

There are 3 argument variants you can use:

=========================== ==================================== ===============================================================================================================
Mode                        Notation                             Value
=========================== ==================================== ===============================================================================================================
``InputArgument.REQUIRED``  none (just write the argument name)  The argument is required
``InputArgument.OPTIONAL``  ``argument?``                        The argument is optional and therefore can be omitted
``InputArgument.IS_LIST``   ``argument*``                        The argument can contain an indefinite number of arguments and must be used at the end of the argument list
=========================== ==================================== ===============================================================================================================

You can combine ``IS_LIST`` with ``REQUIRED`` and ``OPTIONAL`` like this:

.. code-block:: python

    class GreetCommand(Command):
        """
        Greets someone

        demo:greet
            {names?* : Who do you want to greet?}
            {--y|yell : If set, the task will yell in uppercase letters}
        """

If you want to set a default value, you can it like so:

.. code-block:: text

    argument=default

The argument will then be considered optional.


Using Options
-------------

Unlike arguments, options are not ordered (meaning you can specify them in any
order) and are specified with two dashes (e.g. ``--yell`` - you can also
declare a one-letter shortcut that you can call with a single dash like
``-y``). Options are *always* optional, and can be setup to accept a value
(e.g. ``--dir=src``) or simply as a boolean flag without a value (e.g.
``--yell``).

.. tip::

    It is also possible to make an option *optionally* accept a value (so that
    ``--yell`` or ``--yell=loud`` work). Options can also be configured to
    accept a list of values.

For example, add a new option to the command that can be used to specify
how many times in a row the message should be printed:

.. code-block:: python

    class GreetCommand(Command):
        """
        Greets someone

        demo:greet
            {name? : Who do you want to greet?}
            {--y|yell : If set, the task will yell in uppercase letters}
            {--iterations=1 : How many times should the message be printed?}
        """


Next, use this in the command to print the message multiple times:

.. code-block:: python

    for _ in range(0, self.option('iterations')):
        self.line(text)

Now, when you run the task, you can optionally specify a ``--iterations``
flag:

.. code-block:: bash

    $ python application.py demo:greet John
    $ python application.py demo:greet John --iterations=5

The first example will only print once, since ``iterations`` is empty and
defaults to ``1``. The second example will print five times.

Recall that options don't care about their order. So, either of the following
will work:

.. code-block:: bash

    $ python application.py demo:greet John --iterations=5 --yell
    $ python application.py demo:greet John --yell --iterations=5

There are 4 option variants you can use:

===============================  =================================== ======================================================================================
Option                           Notation                            Value
===============================  =================================== ======================================================================================
``InputOption.VALUE_IS_LIST``    ``--option=*``                      This option accepts multiple values (e.g. ``--dir=/foo --dir=/bar``)
``InputOption.VALUE_NONE``       ``--option``                        Do not accept input for this option (e.g. ``--yell``)
``InputOption.VALUE_REQUIRED``   ``--option=``                       This value is required (e.g. ``--iterations=5``), the option itself is still optional
``InputOption.VALUE_OPTIONAL``   ``--option=?``                      This option may or may not have a value (e.g. ``--yell`` or ``--yell=loud``)
===============================  =================================== ======================================================================================

You can combine ``VALUE_IS_LIST`` with ``VALUE_REQUIRED`` or ``VALUE_OPTIONAL`` like this:

.. code-block:: python

    class GreetCommand(Command):
        """
        Greets someone

        demo:greet
            {name? : Who do you want to greet?}
            {--y|yell : If set, the task will yell in uppercase letters}
            {--iterations=?*1 : How many times should the message be printed?}
        """


Testing Commands
----------------

Cleo provides several tools to help you test your commands. The most
useful one is the ``CommandTester`` class.
It uses special input and output classes to ease testing without a real
console:

.. code-block:: python

    from unittest import TestCase
    from cleo import Application, CommandTester

    class GreetCommandTest(TestCase):

        def test_execute(self):
            application = Application()
            application.add(GreetCommand())

            command = application.find('demo:greet')
            command_tester = CommandTester(command)
            command_tester.execute([('command', command.get_name())])

            self.assertRegex('...', command_tester.get_display())

            # ...

The ``CommandTester.get_display()`` method returns what would have been displayed
during a normal call from the console.

You can test sending arguments and options to the command by passing them
as an list of tuples to the ``CommandTester.execute()`` method:

.. code-block:: python

    from unittest import TestCase
    from cleo import Application, CommandTester

    class GreetCommandTest(TestCase):

        def test_name_is_output(self):
            application = Application()
            application.add(GreetCommand())

            commmand = application.find('demo:greet')
            command_tester = CommandTester(command)
            command_tester.execute([
                ('command', command.get_name()),
                ('name', 'John')
            ])

            self.assertRegex('John', command_tester.get_display())

You can also test a whole console application by using the ``ApplicationTester`` class.


Calling an existing Command
---------------------------

If a command depends on another one being run before it, instead of asking the
user to remember the order of execution, you can call it directly yourself.
This is also useful if you want to create a "meta" command that just runs a
bunch of other commands.

Calling a command from another one is straightforward:

.. code-block:: python

    def handle(self):
        return_code = self.call('demo:greet', [
            ('name', 'John'),
            ('--yell', True)
        ])

        # ...

If you want to suppress the output of the executed command,
you can use the ``call_silent()`` method instead.



Autocompletion
--------------

Cleo supports automatic (tab) completion in ``bash`` and ``zsh``.

To activate support for autocompletion, pass a ``complete`` keyword when initializing
your application:

.. code-block:: python

    application = Application('My Application', '0.1', complete=True)

Now, register completion for your application by running one of the following in a terminal,
replacing ``[program]`` with the command you use to run your application:

.. code-block:: bash

    # BASH ~4.x, ZSH
    source <([program] _completion --generate-hook)

    # BASH ~3.x, ZSH
    [program] _completion --generate-hook | source /dev/stdin

    # BASH (any version)
    eval $([program] _completion --generate-hook)

By default this registers completion for the absolute path to you application,
which will work if the program is accessible on your PATH.
You can specify a program name to complete for instead using the ``-p\--program`` option,
which is required if you're using an alias to run the program.

If you want the completion to apply automatically for all new shell sessions,
add the command to your shell's profile (eg. ``~/.bash_profile`` or ``~/.zshrc``)

The type of shell (zsh/bash) is automatically detected using the ``SHELL`` environment variable at run time.
In some circumstances, you may need to explicitly specify the shell type with the ``--shell-type`` option.
