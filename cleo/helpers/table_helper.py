# -*- coding: utf-8 -*-

import warnings
from .helper import Helper
from .table import Table
from ..outputs import NullOutput


class TableHelper(Helper):
    """
    Provides helpers to display table output.
    """

    LAYOUT_DEFAULT = 0
    LAYOUT_BORDERLESS = 1
    LAYOUT_COMPACT = 2

    def __init__(self):
        warnings.warn('TableHelper class is deprecated. '
                      'Use the Table class instead', DeprecationWarning)

        self._table = Table(NullOutput())


    def set_layout(self, layout):
        """
        Sets table layout type.

        :param layout: self.LAYOUT_*
        :type layout: int

        :rtype: TableHelper
        """
        if layout == self.LAYOUT_BORDERLESS:
            self._table.set_style('borderless')
        elif layout == self.LAYOUT_COMPACT:
            self._table.set_style('compact')
        elif layout == self.LAYOUT_DEFAULT:
            self._table.set_style('default')
        else:
            raise Exception('Invalid table layout "%s".' % layout)

        return self

    def set_headers(self, headers):
        self._table.set_headers(headers)

        return self

    def set_rows(self, rows):
        self._table.set_rows(rows)

        return self

    def add_rows(self, rows):
        self._table.add_rows(rows)

        return self

    def add_row(self, row):
        self._table.add_row(row)

        return self

    def set_row(self, column, row):
        self._table.set_row(column, row)

        return self

    def set_padding_char(self, padding_char):
        self._table.get_style().set_padding_char(padding_char)

        return self

    def set_horizontal_border_char(self, horizontal_border_char):
        self._table.get_style().set_horizontal_border_char(horizontal_border_char)

        return self

    def set_vertical_border_char(self, vertical_border_char):
        self._table.get_style().set_vertical_border_char(vertical_border_char)

        return self

    def set_crossing_char(self, crossing_char):
        self._table.get_style().set_crossing_char(crossing_char)

        return self

    def set_cell_header_format(self, cell_header_format):
        self._table.get_style().set_cell_header_format(cell_header_format)

        return self

    def set_cell_row_format(self, cell_row_format):
        self._table.get_style().set_cell_row_format(cell_row_format)

        return self

    def set_cell_row_content_format(self, cell_row_content_format):
        self._table.get_style().set_cell_row_content_format(cell_row_content_format)

        return self

    def set_border_format(self, border_format):
        self._table.get_style().set_border_format(border_format)

        return self

    def set_pad_type(self, pad_type):
        self._table.get_style().set_pad_type(pad_type)

        return self

    def render(self, output):
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

        :param output_: Output
        :type output_: Output
        """
        self._table._output = output

        return self._table.render()

    def get_name(self):
        return 'table'
