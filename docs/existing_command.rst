Calling an existing Command
---------------------------

If a command depends on another one being run before it, instead of asking the
user to remember the order of execution, you can call it directly yourself.
This is also useful if you want to create a "meta" command that just runs a
bunch of other commands.

.. note::

    This is only possible when declaring command via classes and not via dictionaries
    since you need to have access to the command instance.

Calling a command from another one is straightforward:

.. code-block:: python

    def execute(i, o):
        command = self.get_application().find('demo:greet')

        arguments = [
            ('command', command.get_name()),
            ('name', 'John'),
            ('--yell', True)
        ]

        greet_input = ListInput(arguments)
        return_code = command.run(greet_input, o)

        # ...

First, you find (with ``Application.find()``) the
command you want to execute by passing the command name.

Then, you need to create a new ``ListInput`` instance
with the arguments and options you want to pass to the command.

Eventually, calling the ``run()`` method actually executes the command and
returns the returned code from the command (return value from command's
``execute()`` method).
