Building a Single Command Application
=====================================

When building a command line tool, you may not need to provide several commands.
In such case, having to pass the command name each time is tedious. Fortunately,
it is possible to remove this need by extending the application:

.. code-block:: python

    from cleo import Application

    class MyApplication(Application):

        def get_command_name(i):
            """
            Gets the name of the command based in input.
            """
            # This should return the name of your command
            return 'my_command'

        def get_default_commands():
            """
            Gets the default commands that should always be available.
            """
            # Keep the core default commands to have the HelpCommand
            # which is used when using the --help option
            default_commands = super(MyApplication, self).get_default_commands()

            default_commands.append(MyCommand())

            return default_commands

        def get_definition():
            """
            Overridden so that the application doesn't expect the command
            name to be the first argument.
            """
            idefinition = super(MyApplication, self).get_definition()
            # Clear out the normal first argument, which is the command name
            idefinition.set_arguments()

            return idefinition


When calling your console script, the command ``MyCommand`` will then always
be used, without having to pass its name.

You can also simplify how you execute the application:

.. code-block:: python

    #!/usr/bin/env ython

    application = MyApplication()
    application.run()
