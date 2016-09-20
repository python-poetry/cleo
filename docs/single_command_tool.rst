Building a Single Command Application
#####################################

When building a command line tool, you may not need to provide several commands.
In such case, having to pass the command name each time is tedious. Fortunately,
it is possible to remove this need by using the `set_default_command()` method:

.. code-block:: python

    from cleo import Application

    command = GreetCommand()

    app = Application()
    app.add(commmand)

    # the second boolean argument tells if this is a single-command app
    app.set_default_command(command.get_name(), True)

    # this now executes the 'GreetCommand' without passing its name
    app.run()
