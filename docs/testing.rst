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
            application.add(greet_command)
            # Or application.add(GreetCommand()) if using classes

            commmand = application.find('demo:greet')
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
            application.add(greet_command)
            # Or application.add(GreetCommand()) if using classes

            commmand = application.find('demo:greet')
            command_tester = CommandTester(command)
            command_tester.execute([
                ('command', command.get_name()),
                ('name', 'John')
            ])

            self.assertRegex('John', command_tester.get_display())

.. tip::

    You can also test a whole console application by using the ``ApplicationTester`` class.
