Using Arguments
---------------

.. role:: python(code)
   :language: python

The most interesting part of the commands are the arguments and options that
you can make available. Arguments are the strings - separated by spaces - that
come after the command name itself. They are ordered, and can be optional
or required. For example, add an optional ``last_name`` argument to the command
and make the ``name`` argument required:

.. code-block:: python

    'arguments': [{
        'name': 'name',
        'description': 'Who do you want to greet?',
        'required': False
    }, {
        'name': 'last_name',
        'description': 'Your last name?',
        'required': False
    }]

    # Class notation
    self
        # ...
        .add_argument(
            'name',
            InputArgument.REQUIRED,
            'Who do you want to greet?'
        )\
        .add_argument(
            'last_name',
            InputArgument.OPTIONAL,
            'Your last name?'
        )

.. versionadded:: 0.3

    Decorators notation.

    .. code-block:: python

        from cleo import Application

        app = Application()

        @app.command('demo:greet', description='Greets someone')
        @app.argument('last_name', description='Your last name?', required=False)
        @app.argument('name', description='Who do you want to greet?', required=True)
        def greet(i, o):
            # ...

You now have access to a ``last_name`` argument in your command:

.. code-block:: python

    last_name = i.get_argument('last_name')
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

    'arguments': [{
        'name': 'names',
        'description': 'Who do you want to greet (separate multiple names with a space)?',
        'list': True
    }]

    # Class notation
    self
        # ...
        .add_argument(
            'names',
            InputArgument.IS_LIST,
            'Who do you want to greet (separate multiple names with a space)?'
        )

To use this, just specify as many names as you want:

.. code-block:: bash

    $ python application.py demo:greet John Jane

You can access the ``names`` argument as a list:

.. code-block:: python

    names = i.get_argument('name')
    if names:
        text += ' %s' % ', '.join(names)
    }

There are 3 argument variants you can use:

=========================== ============================== ===============================================================================================================
Mode                        Dictionary notation            Value
=========================== ============================== ===============================================================================================================
``InputArgument.REQUIRED``  :python:`{'required': True}`   The argument is required
``InputArgument.OPTIONAL``  :python:`{'required': False}`  The argument is optional and therefore can be omitted
``InputArgument.IS_LIST``   :python:`{'list': True}`       The argument can contain an indefinite number of arguments and must be used at the end of the argument list
=========================== ============================== ===============================================================================================================

You can combine ``IS_LIST`` with ``REQUIRED`` and ``OPTIONAL`` like this:

.. code-block:: python

    'arguments': [{
        'names': {
            'description': 'Who do you want to greet (separate multiple names with a space)?',
            'required': False,
            'list': True
        }
    }]

    # Class notation
    self
        # ...
        .add_argument(
            'names',
            InputArgument.OPTIONAL | InputArgument.IS_LIST,
            'Who do you want to greet (separate multiple names with a space)?'
        )
