# -*- coding: utf-8 -*-

from .helper import Helper


class TableHelper(Helper):
    """
    Provides helpers to display table output.
    """

    LAYOUT_DEFAULT = 0
    LAYOUT_BORDERLESS = 1
    LAYOUT_COMPACT = 2

    def __init__(self):
        self.__headers = []
        self.__rows = []

        self.__padding_char = ' '
        self.__horizontal_border_char = '-'
        self.__vertical_border_char = '|'
        self.__crossing_char = '+'
        self.__cell_header_format = '<info>%s</info>'
        self.__cell_row_format = '%s'
        self.__cell_row_content_format = ' %s '
        self.__border_format = '%s'
        self.__pad_type = 'right'

        self.__column_widths = []

        self.__number_of_columns = None

        self.__output = None

        self.set_layout(self.LAYOUT_DEFAULT)

    def set_layout(self, layout):
        """
        Sets table layout type.

        @param layout: self.LAYOUT_*
        @type layout: int

        @rtype: TableHelper
        """
        if layout == self.LAYOUT_BORDERLESS:
            self.set_padding_char(' ')\
                .set_horizontal_border_char('=')\
                .set_vertical_border_char(' ')\
                .set_crossing_char(' ')\
                .set_cell_header_format('<info>%s</info>')\
                .set_cell_row_format('%s')\
                .set_cell_row_content_format(' %s ')\
                .set_border_format('%s')\
                .set_pad_type('right')
        elif layout == self.LAYOUT_COMPACT:
            self.set_padding_char(' ')\
                .set_horizontal_border_char('')\
                .set_vertical_border_char(' ')\
                .set_crossing_char('')\
                .set_cell_header_format('<info>%s</info>')\
                .set_cell_row_format('%s')\
                .set_cell_row_content_format('%s')\
                .set_border_format('%s')\
                .set_pad_type('right')
        elif layout == self.LAYOUT_DEFAULT:
            self.set_padding_char(' ')\
                .set_horizontal_border_char('-')\
                .set_vertical_border_char('|')\
                .set_crossing_char('+')\
                .set_cell_header_format('<info>%s</info>')\
                .set_cell_row_format('%s')\
                .set_cell_row_content_format(' %s ')\
                .set_border_format('%s')\
                .set_pad_type('right')
        else:
            raise Exception('Invalid table layout "%s".' % layout)

        return self

    def set_headers(self, headers):
        self.__headers = headers

        return self

    def set_rows(self, rows):
        self.__rows = rows

        return self

    def add_rows(self, rows):
        for row in rows:
            self.add_row(row)

        return self

    def add_row(self, row):
        self.__rows.append(row)

        return self

    def set_row(self, column, row):
        self.__rows[column] = row

        return self

    def set_padding_char(self, padding_char):
        if not padding_char:
            raise Exception('The padding char must not be empty')

        self.__padding_char = padding_char

        return self

    def set_horizontal_border_char(self, horizontal_border_char):
        self.__horizontal_border_char = horizontal_border_char

        return self

    def set_vertical_border_char(self, vertical_border_char):
        self.__vertical_border_char = vertical_border_char

        return self

    def set_crossing_char(self, crossing_char):
        self.__crossing_char = crossing_char

        return self

    def set_cell_header_format(self, cell_header_format):
        self.__cell_header_format = cell_header_format

        return self

    def set_cell_row_format(self, cell_row_format):
        self.__cell_row_format = cell_row_format

        return self

    def set_cell_row_content_format(self, cell_row_content_format):
        self.__cell_row_content_format = cell_row_content_format

        return self

    def set_border_format(self, border_format):
        self.__border_format = border_format

        return self

    def set_pad_type(self, pad_type):
        if pad_type == 'left':
            self.__pad_type = 'rjust'
        elif pad_type == 'right':
            self.__pad_type = 'ljust'
        elif pad_type == 'center':
            self.__pad_type = 'center'
        else:
            raise Exception('Invalid pad type. Must be either "left", "right" or "center".')

        return self

    def render(self, output_):
        """
        Renders table to output.

        Example:

        +---------------+-----------------------+------------------+
        | ISBN          | Title                 | Author           |
        +---------------+-----------------------+------------------+
        | 99921-58-10-7 | Divine Comedy         | Dante Alighieri  |
        | 9971-5-0210-0 | A Tale of Two Cities  | Charles Dickens  |
        | 960-425-059-0 | The Lord of the Rings | J. R. R. Tolkien |
        +---------------+-----------------------+------------------+

        @param output_: Output
        @type output_: Output
        """
        self.__output = output_

        self.render_row_separator()
        self.render_row(self.__headers, self.__cell_header_format)

        if len(self.__headers):
            self.render_row_separator()

        for row in self.__rows:
            self.render_row(row, self.__cell_row_format)

        if len(self.__rows):
            self.render_row_separator()

        self.cleanup()

    def render_row_separator(self):
        """
        Renders horizontal header separator.

        Example: +-----+-----------+-------+
        """
        count = self.get_number_of_columns()
        if not count:
            return

        if not self.__horizontal_border_char and not self.__crossing_char:
            return

        markup = self.__crossing_char
        for column in range(0, count):
            markup += self.__horizontal_border_char * self.get_column_width(column) + self.__crossing_char

        self.__output.writeln(self.__border_format % markup)

    def render_column_separator(self):
        """
        Renders vertical column separator.
        """
        self.__output.write(self.__border_format % self.__vertical_border_char)

    def render_row(self, row, cell_format):
        """
        Renders table row.

        Example: | 9971-5-0210-0 | A Tale of Two Cities  | Charles Dickens  |

        @param row: The row to render
        @type: row: list
        @param cell_format: The cell format
        @type cell_format: str
        """
        if not row:
            return

        self.render_column_separator()

        count = self.get_number_of_columns()
        for column in range(0, count):
            self.render_cell(row, column, cell_format)
            self.render_column_separator()

        self.__output.writeln('')

    def render_cell(self, row, column, cell_format):
        """
        Renders table cell with padding.

        @param row: The row to render
        @type: row: list
        @param column: The column to render
        @param cell_format: The cell format
        @type cell_format: str
        """
        try:
            cell = row[column]
        except IndexError:
            cell = ''

        width = self.get_column_width(column)

        content = self.__cell_row_content_format % cell

        self.__output.write(cell_format % getattr(content, self.__pad_type)(width, self.__padding_char))

    def get_number_of_columns(self):
        """
        Gets the number of columns for this table.

        @rtype: int
        """
        if self.__number_of_columns is not None:
            return self.__number_of_columns

        columns = [0, len(self.__headers)]
        for row in self.__rows:
            columns.append(len(row))

        self.__number_of_columns = max(columns)

        return self.__number_of_columns

    def get_column_width(self, column):
        try:
            return self.__column_widths[column]
        except IndexError:
            lengths = [0, self.get_cell_width(self.__headers, column)]
            for row in self.__rows:
                lengths.append(self.get_cell_width(row, column))

            self.__column_widths.insert(column, max(lengths) + len(self.__cell_row_content_format) - 2)

            return self.__column_widths[column]

    def get_cell_width(self, row, column):
        if column < 0:
            return 0

        if column < len(row):
            return len(row[column])

        return self.get_cell_width(row, column - 1)

    def cleanup(self):
        self.__column_widths = []
        self.__number_of_columns = None

    def get_name(self):
        return 'table'
