Formatter Helper
################

The Formatter helper provides functions to format the output with colors.
You can do more advanced things with this helper than you can in
:ref:`output-coloring`.

The ``FormatterHelper`` class is included
in the default helper set, which you can get by calling
``Command.get_helper()``:

.. code-block:: python

    formatter = self.get_helper('formatter')

The methods return a string, which you'll usually render to the console by
passing it to the ``line()`` method.

Print Messages in a Section
===========================

Cleo offers a defined style when printing a message that belongs to some
"section". It prints the section in color and with brackets around it and the
actual message to the right of this. Minus the color, it looks like this:

.. code-block:: text

    [SomeSection] Here is some message related to that section

To reproduce this style, you can use the
``format_section()`` method:

.. code-block:: python

    formatted_line = formatter.format_section(
        'SomeSection',
        'Here is some message related to that section'
    )
    self.line(formatted_line)

Print Messages in a Block
=========================

Sometimes you want to be able to print a whole block of text with a background
color. Cleo uses this when printing error messages.

If you print your error message on more than one line manually, you will
notice that the background is only as long as each individual line. Use the
``format_block()`` method` to generate a block output:

.. code-block:: python

    error_messages = ['Error!', 'Something went wrong']
    formatted_block = formatter.format_block(error_messages, 'error')
    self.line(formatted_block)

As you can see, passing an array of messages to the ``format_block()``
method creates the desired output. If you pass ``True`` as third parameter, the
block will be formatted with more padding (one blank line above and below the
messages and 2 spaces on the left and right).

The exact "style" you use in the block is up to you. In this case, you're using
the pre-defined ``error`` style, but there are other styles, or you can create
your own. See :ref:`output-coloring`.
