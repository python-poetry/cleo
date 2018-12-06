Table
#####

When building a console application it may be useful to display tabular data:

.. code-block:: text

    +---------------+--------------------------+------------------+
    | ISBN          | Title                    | Author           |
    +---------------+--------------------------+------------------+
    | 99921-58-10-7 | Divine Comedy            | Dante Alighieri  |
    | 9971-5-0210-0 | A Tale of Two Cities     | Charles Dickens  |
    | 960-425-059-0 | The Lord of the Rings    | J. R. R. Tolkien |
    | 80-902734-1-6 | And Then There Were None | Agatha Christie  |
    +---------------+--------------------------+------------------+

To display a table, use the ``table()`` method, set the headers, set the rows and then render the table:

.. code-block:: python

    def handle(self):
        table = self.table()

        table.set_header_row(['ISBN', 'Title', 'Author'])
        table.set_rows([
            ['99921-58-10-7', 'Divine Comedy', 'Dante Alighieri'],
            ['9971-5-0210-0', 'A Tale of Two Cities', 'Charles Dickens'],
            ['960-425-059-0', 'The Lord of the Rings', 'J. R. R. Tolkien'],
            ['80-902734-1-6', 'And Then There Were None', 'Agatha Christie']
        ])

        table.render(self.io)

.. tip::

    All these steps can be done in one go using the ``render_table`` method:

    .. code-block:: python

        self.render_table(
            ['ISBN', 'Title', 'Author'],
            [
                ['99921-58-10-7', 'Divine Comedy', 'Dante Alighieri'],
                ['9971-5-0210-0', 'A Tale of Two Cities', 'Charles Dickens'],
                ['960-425-059-0', 'The Lord of the Rings', 'J. R. R. Tolkien'],
                ['80-902734-1-6', 'And Then There Were None', 'Agatha Christie']
            ]
        )

You can add a table separator anywhere in the output by using ``table_seprator()``,
which returns a ``TableSeparator``, as a row:

.. code-block:: python

    table.set_rows([
        ['99921-58-10-7', 'Divine Comedy', 'Dante Alighieri'],
        ['9971-5-0210-0', 'A Tale of Two Cities', 'Charles Dickens'],
        self.table_separator(),
        ['960-425-059-0', 'The Lord of the Rings', 'J. R. R. Tolkien'],
        ['80-902734-1-6', 'And Then There Were None', 'Agatha Christie']
    ])

.. code-block:: text

    +---------------+--------------------------+------------------+
    | ISBN          | Title                    | Author           |
    +---------------+--------------------------+------------------+
    | 99921-58-10-7 | Divine Comedy            | Dante Alighieri  |
    | 9971-5-0210-0 | A Tale of Two Cities     | Charles Dickens  |
    +---------------+--------------------------+------------------+
    | 960-425-059-0 | The Lord of the Rings    | J. R. R. Tolkien |
    | 80-902734-1-6 | And Then There Were None | Agatha Christie  |
    +---------------+--------------------------+------------------+

The table style can be changed to any built-in styles via ``set_style()``:

.. code-block:: python

    # same as calling nothing
    table.set_style('default')

    # changes the default style to compact
    table.set_style('compact')

This code results in:

.. code-block:: text

    ISBN          Title                    Author
    99921-58-10-7 Divine Comedy            Dante Alighieri
    9971-5-0210-0 A Tale of Two Cities     Charles Dickens
    960-425-059-0 The Lord of the Rings    J. R. R. Tolkien
    80-902734-1-6 And Then There Were None Agatha Christie

You can also set the style to ``borderless``:

.. code-block:: python

    table.set_style('borderless')

which outputs:

.. code-block:: text

    =============== ========================== ==================
     ISBN            Title                      Author
    =============== ========================== ==================
     99921-58-10-7   Divine Comedy              Dante Alighieri
     9971-5-0210-0   A Tale of Two Cities       Charles Dickens
     960-425-059-0   The Lord of the Rings      J. R. R. Tolkien
     80-902734-1-6   And Then There Were None   Agatha Christie
    =============== ========================== ==================

If the built-in styles do not fit your need, define your own:

.. code-block:: python

    # by default, this is based on the default style
    style = self.table_style()

    # customize the style
    style.set_horizontal_border_char('<fg=magenta>|</>')
    style.set_vertical_border_char('<fg=magenta>-</>')
    style.set_crossing_char(' ')

    # use the style for this table
    table.set_style(style)

Here is a full list of things you can customize:

*  ``set_adding_char()``
*  ``set_horizontal_border_char()``
*  ``set_vertical_border_char()``
*  ``set_crossing_char()``
*  ``set_cell_header_format()``
*  ``set_cell_row_format()``
*  ``set_border_format()``
*  ``set_pad_type()``

.. tip::

    The style can also be passed as a keyword argument to ``render_table()``

    .. code-block:: python

        self.render_table(
            ['ISBN', 'Title', 'Author'],
            [
                ['99921-58-10-7', 'Divine Comedy', 'Dante Alighieri'],
                ['9971-5-0210-0', 'A Tale of Two Cities', 'Charles Dickens'],
                ['960-425-059-0', 'The Lord of the Rings', 'J. R. R. Tolkien'],
                ['80-902734-1-6', 'And Then There Were None', 'Agatha Christie']
            ]
            style='borderless'
        )


Spanning Multiple Columns and Rows
==================================

To make a table cell that spans multiple columns you can use ``table_cell()``,
which returns a ``TableCell`` instance:

.. code-block:: python

    table = self.table()

    table.set_headers(['ISBN', 'Title', 'Author'])
    table.set_rows([
        ['99921-58-10-7', 'Divine Comedy', 'Dante Alighieri'],
        self.table_separator(),
        [self.table_cell('This value spans 3 columns.', colspan=3)]
    ])

    table.render()

This results in:

.. code-block:: text

    +---------------+---------------+-----------------+
    | ISBN          | Title         | Author          |
    +---------------+---------------+-----------------+
    | 99921-58-10-7 | Divine Comedy | Dante Alighieri |
    +---------------+---------------+-----------------+
    | This value spans 3 columns.                     |
    +---------------+---------------+-----------------+

.. tip::

    You can create a multiple-line page title using a header cell that spans the entire table width:

    .. code-block:: python

        table.set_headers([
            [self.table_cell('Main table title', colspan=3)],
            ['ISBN', 'Title', 'Author']
        ])

    This generate:

    .. code-block:: text

        +-------+-------+--------+
        | Main table title       |
        +-------+-------+--------+
        | ISBN  | Title | Author |
        +-------+-------+--------+
        | ...                    |
        +-------+-------+--------+

In a similar way you can span multiple rows:

.. code-block:: python

    table = self.table()

    table.set_headers(['ISBN', 'Title', 'Author'])
    table.set_rows([
        [
            '978-0521567817',
            'De Monarchia',
            self.table_cell('Dante Alighieri\nspans multiple rows', rowspan=2)
        ]
    ])

    table.render()

This outputs:

.. code-block:: text

    +----------------+---------------+---------------------+
    | ISBN           | Title         | Author              |
    +----------------+---------------+---------------------+
    | 978-0521567817 | De Monarchia  | Dante Alighieri     |
    | 978-0804169127 | Divine Comedy | spans multiple rows |
    +----------------+---------------+---------------------+

You can use the ``colspan`` and ``rowspan`` options at the same time
which allows you to create any table layout you may wish.
