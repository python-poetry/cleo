Using Console Commands, Shortcuts and Built-in Commands
#######################################################

In addition to the options you specify for your commands, there are some
built-in options as well as a couple of built-in commands for Cleo.

.. note::

    These examples assume you have added a file ``application.py`` to run at
    the cli:
    
    .. code-block:: python

        #!/usr/bin/env python
        # application.py

        from cleo import Application

        application = Application()
        # ...
        
        if __name__ == '__main__':
            application.run()

Built-in Commands
=================

The help command lists the help information for the specified command. For
example, to get the help for the ``list`` command:

.. code-block:: bash

    $ python application.py help list

Running ``help`` without specifying a command will list the global options:

.. code-block:: bash

    $ python application.py help


Global Options
==============

You can get help information for any command with the ``--help`` option. To
get help for the ``greet`` command:

.. code-block:: bash

    $ python application.py greet --help
    $ python application.py greet -h

You can suppress output with:

.. code-block:: bash

    $ python application.py greet --quiet
    $ python application.py greet -q

You can get more verbose messages (if this is supported for a command)
with:

.. code-block:: bash

    $ python application.py greet --verbose
    $ python application.py greet -v

If you need more verbose output, use `-vv` or `-vvv`

.. code-block:: bash

    $ python application.py greet -vv
    $ python application.py greet -vvv

If you set the optional arguments to give your application a name and version:

.. code-block:: python

    application = Application('console', '1.2')

then you can use:

.. code-block:: bash

    $ python application.py --version
    $ python application.py -V

to get this information output:

.. code-block:: text

    Console version 1.2

If you do not provide both arguments then it will just output:

.. code-block:: text

    console tool

You can force turning on ANSI output coloring with:

.. code-block:: bash

    $ python application.py greet --ansi

or turn it off with:

.. code-block:: bash

    $ python application.py greet --no-ansi

You can suppress any interactive questions from the command you are running with:

.. code-block:: bash

    $ python application.py greet --no-interaction
    $ python application.py greet -n


Shortcut Syntax
===============

You do not have to type out the full command names. You can just type the
shortest unambiguous name to run a command. So if there are non-clashing
commands, then you can run ``help`` like this:

.. code-block:: bash

    $ python application.py h
