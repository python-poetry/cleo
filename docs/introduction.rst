Usage
#####

To make a command that greets you from the command line,
create ``greet_command.py`` and add the following to it:

.. code-block:: python

    from cleo import Command


    class GreetCommand(Command):
        """
        Greets someone

        greet
            {name? : Who do you want to greet?}
            {--y|yell : If set, the task will yell in uppercase letters}
        """

        def handle(self):
            name = self.argument('name')

            if name:
                text = 'Hello {}'.format(name)
            else:
                text = 'Hello'

            if self.option('yell'):
                text = text.upper()

            self.line(text)


You also need to create the file to run at the command line which creates
an ``Application`` and adds commands to it:

.. code-block:: python

    #!/usr/bin/env python

    from greet_command import GreetCommand
    from cleo import Application

    application = Application()
    application.add(GreetCommand())

    if __name__ == '__main__':
        application.run()

Test the new command by running the following

.. code-block:: bash

    $ python application.py greet John

This will print the following to the command line:

.. code-block:: text

    Hello John

You can also use the ``--yell`` option to make everything uppercase:

.. code-block:: bash

    $ python application.py greet John --yell

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
===================

Whenever you output text, you can surround the text with tags to color its
output. For example:

.. code-block:: python

    # blue text
    self.line("<info>foo</info>")

    # green text
    self.line("<comment>foo</comment>")

    # cyan text
    self.line("<question>foo</question>")

    # bold red text
    self.line("<error>foo</error>")

    # cyan text
    self.line("<c1>foo</c1>")

    # bold text
    self.line("<c2>foo</c2>")

    # bold text
    self.line("<b>foo</b>")

The closing tag can be replaced by ``</>``, which revokes all formatting options established by the last opened tag.

It is possible to define your own styles using the ``add_style()`` method:

.. code-block:: python

    self.add_style('fire', fg='red', bg='yellow', options=['bold', 'blink'])
    self.line('<fire>foo</fire>')

Available foreground and background colors are: ``black``, ``red``, ``green``,
``yellow``, ``blue``, ``magenta``, ``cyan`` and ``white``.

And available options are: ``bold``, ``underscore``, ``blink``, ``reverse`` and ``conceal``.

You can also set these colors and options inside the tag name:

.. code-block:: python

    # green text
    self.line('<fg=green>foo</>')

    # black text on a cyan background
    self.line('<fg=black;bg=cyan>foo</>')

    # bold text on a yellow background
    self.line('<bg=yellow;options=bold>foo</>')


Verbosity Levels
================

Cleo has four verbosity levels. These are defined in the ``Output`` class:

=======================================  ================================== ======================
Mode                                     Meaning                            Console option
=======================================  ================================== ======================
``NA``                                   Do not output any messages         ``-q`` or ``--quiet``
``Verbosity.NORMAL``                     The default verbosity level        (none)
``Verbosity.VERBOSE``                    Increased verbosity of messages    ``-v``
``Verbosity.VERY_VERBOSE``               Informative non essential messages ``-vv``
``Verbosity.DEBUG``                      Debug messages                     ``-vvv``
=======================================  ================================== ======================

It is possible to print a message in a command for only a specific verbosity
level. For example:

.. code-block:: python

    if Verbosity.VERBOSE <= self.io.verbosity:
        self.line(...)

There are also more semantic methods you can use to test for each of the
verbosity levels:

.. code-block:: python

    if self.output.is_quiet():
        # ...

    if self.output.is_verbose():
        # ...

You can also pass the verbosity flag directly to `line()`.

.. code-block:: python

    self.line("", verbosity=Verbosity.VERBOSE)

When the quiet level is used, all output is suppressed.


Using Arguments
===============

The most interesting part of the commands are the arguments and options that
you can make available. Arguments are the strings - separated by spaces - that
come after the command name itself. They are ordered, and can be optional
or required. For example, add an optional ``last_name`` argument to the command
and make the ``name`` argument required:

.. code-block:: python

    class GreetCommand(Command):
        """
        Greets someone

        greet
            {name : Who do you want to greet?}
            {last_name? : Your last name?}
            {--y|yell : If set, the task will yell in uppercase letters}
        """

You now have access to a ``last_name`` argument in your command:

.. code-block:: python

    last_name = self.argument('last_name')
    if last_name:
        text += ' {}'.format(last_name)

The command can now be used in either of the following ways:

.. code-block:: bash

    $ python application.py greet John
    $ python application.py greet John Doe

It is also possible to let an argument take a list of values (imagine you want
to greet all your friends). For this it must be specified at the end of the
argument list:

.. code-block:: python

    class GreetCommand(Command):
        """
        Greets someone

        greet
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
        text += ' {}'.format(', '.join(names))

There are 3 argument variants you can use:

================================ ==================================== ===============================================================================================================
Mode                             Notation                             Value
================================ ==================================== ===============================================================================================================
``Required``                     none (just write the argument name)  The argument is required
``Optional``                     ``argument?``                        The argument is optional and therefore can be omitted
``List``                         ``argument*``                        The argument can contain an indefinite number of arguments and must be used at the end of the argument list
================================ ==================================== ===============================================================================================================

You can combine them like this:

.. code-block:: python

    class GreetCommand(Command):
        """
        Greets someone

        greet
            {names?* : Who do you want to greet?}
            {--y|yell : If set, the task will yell in uppercase letters}
        """

If you want to set a default value, you can it like so:

.. code-block:: text

    argument=default

The argument will then be considered optional.


Using Options
=============

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

        greet
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

================================  =================================== ======================================================================================
Option                            Notation                            Value
================================  =================================== ======================================================================================
``List``                          ``--option=*``                      This option accepts multiple values (e.g. ``--dir=/foo --dir=/bar``)
``Flag``                          ``--option``                        Do not accept input for this option (e.g. ``--yell``)
``Requires value``                ``--option=``                       This value is required (e.g. ``--iterations=5``), the option itself is still optional
``Optional value``                ``--option=?``                      This option may or may not have a value (e.g. ``--yell`` or ``--yell=loud``)
================================  =================================== ======================================================================================

You can combine them like this:

.. code-block:: python

    class GreetCommand(Command):
        """
        Greets someone

        greet
            {name? : Who do you want to greet?}
            {--y|yell : If set, the task will yell in uppercase letters}
            {--iterations=?*1 : How many times should the message be printed?}
        """


Helpers
=======

Cleo also contains a set of "helpers" - different small
tools capable of helping you with different tasks:

* :doc:`helpers/question_helper`: interactively ask the user for information
* :doc:`helpers/progress_bar`: shows a progress bar
* :doc:`helpers/table`: displays tabular data as a table


Testing Commands
================

Cleo provides several tools to help you test your commands. The most
useful one is the ``CommandTester`` class.
It uses a special IO class to ease testing without a real
console:

.. code-block:: python

    import pytest

    from cleo import Application
    from cleo.testers.command_tester import CommandTester

    def test_execute(self):
        application = Application()
        application.add(GreetCommand())

        command = application.find('demo:greet')
        command_tester = CommandTester(command)
        command_tester.execute()

        assert "..." == command_tester.io.fetch_output()

The ``CommandTester.io.fetch_output()`` method returns what would have been displayed
during a normal call from the console. ``CommandTester.io.fetch_error()`` is also available
to get what you have been written to the stderr.

You can test sending arguments and options to the command by passing them
as a string to the ``CommandTester.execute()`` method:

.. code-block:: python

    import pytest

    from cleo import Application
    from cleo.testers.command_tester import CommandTester

    def test_execute(self):
        application = Application()
        application.add(GreetCommand())

        command = application.find('demo:greet')
        command_tester = CommandTester(command)
        command_tester.execute("John")

        assert "John" in command_tester.io.fetch_output()


Testing with user inputs
------------------------

To test user inputs, you pass it to ``execute()``.

.. code-block:: python

    command_tester = CommandTester(command)
    command_tester.execute(inputs="123\nfoo\nbar")

.. tip::

    You can also test a whole console application by using the ``ApplicationTester`` class.


Calling an existing Command
===========================

If a command depends on another one being run before it, instead of asking the
user to remember the order of execution, you can call it directly yourself.
This is also useful if you want to create a "meta" command that just runs a
bunch of other commands.

Calling a command from another one is straightforward:

.. code-block:: python

    def handle(self):
        return_code = self.call('demo:greet', "John --yell")

        # ...

.. tip::

    If you want to suppress the output of the executed command,
    you can use the ``call_silent()`` method instead.


Overwrite the current line
==========================

If you want to overwrite the current line, you can use the ``overwrite()`` method.

.. code-block:: python

    def handle(self):
        self.write('Processing...')
        # do some work
        self.overwrite('Done!')

.. warning::

    ``overwrite()`` will only work in combination with the ``write()`` method which does not
    add a new line.

.. note::

    ``overwrite()`` does not automatically add a new line so you must call ``line('')`` if necessary.


Autocompletion
==============

Cleo supports automatic (tab) completion in ``bash``, ``zsh`` and ``fish``.

By default, your application will have a ``completions`` command. To register these completions for your application, run one of the following in a terminal (replacing ``[program]`` with the command you use to run your application):

.. code-block:: bash

    # Bash
    [program] completions bash | sudo tee /etc/bash_completion.d/[program].bash-completion

    # Bash - macOS/Homebrew (requires `brew install bash-completion`)
    [program] completions bash > $(brew --prefix)/etc/bash_completion.d/[program].bash-completion

    # Zsh
    mkdir ~/.zfunc
    echo "fpath+=~/.zfunc" >> ~/.zshrc
    [program] completions zsh > ~/.zfunc/_[program]

    # Zsh - macOS/Homebrew
    [program] completions zsh > $(brew --prefix)/share/zsh/site-functions/_[program]

    # Fish
    [program] completions fish > ~/.config/fish/completions/[program].fish
