Validators
##########

Validators are a convenient way to check and adapt the type of an argument or an option.

.. code-block:: python

    class GreetCommand(Command):
        """
        Greets someone

        demo:greet {name? : Who do you want to greet?}
                   {--y|yell : If set, will yell in uppercase letters}
                   {--iterations=1 (integer) : How many times should the message be printed?}
        """

When using validators inside a command signature, only the :ref:`named_validators` are supported.
Validators must be specified like so:

.. code-block:: text

    {argument_or_option (validator)}

If you need more complex validators, or want to specify options to validators, you can do so by
using the ``validation`` attribute:

.. code-block:: python

    class GreetCommand(Command):
        """
        Greets someone

        demo:greet {name? : Who do you want to greet?}
                   {--y|yell : If set, will yell in uppercase letters}
                   {--iterations=1 : How many times should the message be printed?}
        """

        validation = {
            '--iterations': Integer()
        }

For now, there are only a few built-in validators:

.. note::

    It is important to note that there is no ``String()`` validator. The reason is quite simple:
    By default, the command line arguments and options are considered strings, so there is no need
    to specify it.


Integer and Float
=================

Those validators are self-explanatory.


Boolean
=======

The ``Boolean()`` validator only accepts the following values: ``1``, ``true``, ``yes``, ``y``, ``on``
and their negatives (``0``, ``no``, ``n``, ``off``) or native boolean types (``True``, ``False``).


Range
=====

The ``Range()`` validator accepts a value that must be comprised inside a specified range.

The range can be of anything that can be compared to the specified value, like integers, floats or string.

The default validator for ranges is ``Integer`` but it can be changed.


.. code-block:: python

    # Not including the boundaries
    Range(0, 6, include_min=False, include_max=False))

    # Float validator
    Range(12.34, 56.78, validator=Float())

    # String validator (just pass None as validator value)
    Range('c', 'h', validator=None)


Choice/Enum
===========

The ``Choice()`` (or its alias ``Enum``) restricts a possible value to a specified set of choices.


.. code-block:: python

    Choice(['orange', 'blue', 'yellow'])

    # With validator
    Choice([1, 3, 5, 7, 11], validator=Integer())


.. _named_validators:

Named Validators
================

Instead of declaring explicitely the validators it is possible to use their internal names:

    * ``Boolean``: ``boolean``
    * ``Integer``: ``integer``
    * ``Float``: ``boolean``
    * ``Choice/Enum``: ``choice`` or ``enum``
    * ``Range``: ``range``

.. note::

    When using named validators, the corresponding generated validator will have its default options.
