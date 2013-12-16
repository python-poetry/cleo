Cleo
====

Cleo is a Python port of the [Symfony Console Component](https://github.com/symfony/Console).
It eases the creation of beautiful and testable command line interfaces.

The Application object manages the CLI application:

    from cleo import Application

    console = Application()
    console.run()

The ``run()`` method parses the arguments and options passed on the command
line and executes the right command.

Registering a new command can easily be done via the ``register()`` method,
which returns a ``Command`` instance:

    from cleo.input import InputArgument, InputOption

    def ls_dir(input_, output_):
        dir = input_.get_argument('dir')

        output_.writeln('Dir listing for <info>%s</info>' % dir)

    console\
        .register('ls')\
        .set_definition([
            InputArgument('dir', InputArgument.REQUIRED, 'Directory name'),
        ])\
        .set_description('Displays the files in the given directory')\
        .set_code(ls_dir)

You can also register new commands via classes.

Cleo provides a lot of features like output coloring, input and
output abstractions (so that you can easily unit-test your commands),
validation, automatic help messages, ...

Tests
-----

You can run the unit tests with the following command:

    $ nosetests tests
