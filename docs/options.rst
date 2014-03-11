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

    'options': [{
        'iterations': {
            'description': 'How many times should the message be printed?',
            'value_required': True,
            'default': 1
        }
    }]

    # Class notation
    self.
        # ...
        .add_option(
            'iterations',
            None,
            InputOption.VALUE_REQUIRED,
            'How many times should the message be printed?',
            1
        )

Next, use this in the command to print the message multiple times:

.. code-block:: python

    for _ in range(0, input.get_option('iterations')):
        output_.writeln(text)

Now, when you run the task, you can optionally specify a ``--iterations``
flag:

.. code-block:: bash

    $ python application.py demo:greet John
    $ python application.py demo:greet John --iterations=5

.. note::

    Naturally, the ``--iterations=5`` part can also be written ``--iterations 5``

The first example will only print once, since ``iterations`` is empty and
defaults to ``1``. The second example will print five times.

Recall that options don't care about their order. So, either of the following
will work:

.. code-block:: bash

    $ python application.py demo:greet John --iterations=5 --yell
    $ python application.py demo:greet John --yell --iterations=5

There are 4 option variants you can use:

===========================  ======================== ======================================================================================
Option                       Dictionary notation      Value
===========================  ======================== ======================================================================================
InputOption.VALUE_IS_LIST    'list': True             This option accepts multiple values (e.g. ``--dir=/foo --dir=/bar``)
InputOption.VALUE_NONE       'value_required': None   Do not accept input for this option (e.g. ``--yell``)
InputOption.VALUE_REQUIRED   'value_required': True   This value is required (e.g. ``--iterations=5``), the option itself is still optional
InputOption.VALUE_OPTIONAL   'value_required': False  This option may or may not have a value (e.g. ``--yell`` or ``--yell=loud``)
===========================  ======================== ======================================================================================

You can combine ``VALUE_IS_ARRAY`` with ``VALUE_REQUIRED`` or ``VALUE_OPTIONAL`` like this:

.. code-block:: python

    'options': [{
        'iterations': {
            'description': 'How many times should the message be printed?',
            'value_required': True,
            'list': True
            'default': [1]
        }
    }]

    # Class notation
    self.
        # ...
        .add_option(
            'iterations',
            None,
            InputOption.VALUE_REQUIRED | InputOption.VALUE_IS_LIST,
            'How many times should the message be printed?',
            [1]
        )
