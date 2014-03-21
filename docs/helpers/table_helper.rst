Table Helper
============

When building a console application it may be useful to display tabular data:

To display a table, use the ``TableHelper`` class,
set headers, rows and render:

.. code-block:: python

    table = app.get_helper_set().get('table')
    table
        .set_headers(['ISBN', 'Title', 'Author'])
        .set_rows([
           ['99921-58-10-7', 'Divine Comedy', 'Dante Alighieri'],
           ['9971-5-0210-0', 'A Tale of Two Cities', 'Charles Dickens'],
           ['960-425-059-0', 'The Lord of the Rings', 'J. R. R. Tolkien'],
           ['80-902734-1-6', 'And Then There Were None', 'Agatha Christie']
        ])

    table.render(output_)

The table layout can be customized as well. There are two ways to customize
table rendering: using named layouts or by customizing rendering options.

Customize Table Layout using Named Layouts
------------------------------------------

The Table helper ships with three preconfigured table layouts:

* ``TableHelper.LAYOUT_DEFAULT``

* ``TableHelper.LAYOUT_BORDERLESS``

* ``TableHelper.LAYOUT_COMPACT``

Layout can be set using the ``TableHelper.set_layout()`` method.

Customize Table Layout using Rendering Options
----------------------------------------------

You can also control table rendering by setting custom rendering option values:

*  ``TableHelper.set_adding_char()``
*  ``TableHelper.set_horizontal_border_char()``
*  ``TableHelper.set_vertical_border_char()``
*  ``TableHelper.set_crossing_char()``
*  ``TableHelper.set_cell_header_format()``
*  ``TableHelper.set_cell_row_format()``
*  ``TableHelper.set_border_format()``
*  ``TableHelper.set_pad_type()``
