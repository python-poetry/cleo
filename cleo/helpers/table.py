# -*- coding: utf-8 -*-

from __future__ import division

from collections import OrderedDict
from ..exceptions import CleoException
from .table_style import TableStyle
from .table_cell import TableCell
from .table_separator import TableSeparator
from .helper import Helper


class Table(object):
    """
    Provides helpers to display a table.
    """

    styles = None

    def __init__(self, output):
        """
        Constructor.

        :param output: An Output instance
        :type output: Output
        """
        self._output = output
        self._headers = []
        self._rows = []
        self._column_widths = {}
        self._number_of_columns = None
        self._style = None
        self._column_styles = {}

        if not self.__class__.styles:
            self.__class__.styles = self._init_styles()

        self.set_style('default')

    @classmethod
    def set_style_definition(cls, name, table_style):
        """
        Sets a style definition.

        :param name: The name of the style
        :type name: str

        :param table_style: A TableStyle instance
        :type table_style: TableStyle
        """
        if not cls.styles:
            cls.styles = cls._init_styles()

        cls.styles[name] = table_style

    def set_style(self, name):
        """
        Sets table style.

        :param name: The name of the style
        :type name: str
        """
        if isinstance(name, TableStyle):
            self._style = name
        elif name in self.styles:
            self._style = self.styles[name]
        else:
            raise CleoException('Style "%s" is not defined.' % name)

        return self

    def get_style(self):
        """
        :rtype: TableStyle
        """
        return self._style

    def set_column_style(self, column_index, name):
        """
        Sets table column style.

        :param column_index: Colun index
        :type column_index: int

        :param name: The name of the style
        :type name: str or TableStyle

        :rtype: Table
        """
        column_index = int(column_index)

        if isinstance(name, TableStyle):
            self._column_styles[column_index] = name
        elif name in self.styles:
            self._column_styles[column_index] = self.styles[name]
        else:
            raise CleoException('Style "%s" is not defined.' % name)

    def get_column_style(self, column_index):
        """
        Gets the current style for a column.

        If style was not set, it returns the global table style.

        :param column_index: Colun index
        :type column_index: int

        :rtype: TableStyle
        """
        if column_index in self._column_styles:
            return self._column_styles[column_index]

        return self._style

    def set_headers(self, headers):
        if headers and not isinstance(headers[0], list):
            headers = [headers]

        self._headers = headers

        return self

    def set_rows(self, rows):
        self._rows = []

        self.add_rows(rows)

        return self

    def add_rows(self, rows):
        for row in rows:
            self.add_row(row)

        return self

    def add_row(self, row):
        if isinstance(row, TableSeparator):
            self._rows.append(row)

            return self

        if not isinstance(row, list):
            raise CleoException('A row must be a list or a TableSeparator instance.')

        self._rows.append(row)

        return self

    def set_row(self, column, row):
        self._rows[column] = row

        return self

    def render(self):
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
        """
        self._calculate_number_of_columns()
        rows = self._build_table_rows(self._rows)
        headers = self._build_table_rows(self._headers)

        self._calculate_columns_width(headers + rows)

        self._render_row_separator()

        if headers:
            for header in headers:
                self._render_row(header, self._style.cell_header_format)
                self._render_row_separator()

        for row in rows:
            if isinstance(row, TableSeparator):
                self._render_row_separator()
            else:
                self._render_row(row, self._style.cell_row_format)

        if rows:
            self._render_row_separator()

        self._cleanup()

    def _render_row_separator(self):
        """
        Renders horizontal header separator.

        Example: +-----+-----------+-------+
        """
        count = self._number_of_columns
        if not count:
            return

        if not self._style.horizontal_border_char and not self._style.crossing_char:
            return

        markup = self._style.crossing_char
        for column in range(0, count):
            markup += self._style.horizontal_border_char * self._column_widths[column]\
                      + self._style.crossing_char

        self._output.writeln(self._style.border_format % markup)

    def _render_column_separator(self):
        """
        Renders vertical column separator.
        """
        self._output.write(self._style.border_format % self._style.vertical_border_char)

    def _render_row(self, row, cell_format):
        """
        Renders table row.

        Example: | 9971-5-0210-0 | A Tale of Two Cities  | Charles Dickens  |

        :param row: The row to render
        :type: row: list

        :param cell_format: The cell format
        :type cell_format: str
        """
        if not row:
            return

        self._render_column_separator()

        for column in self._get_row_columns(row):
            self._render_cell(row, column, cell_format)
            self._render_column_separator()

        self._output.writeln('')

    def _render_cell(self, row, column, cell_format):
        """
        Renders table cell with padding.

        :param row: The row to render
        :type: row: list

        :param column: The column to render

        :param cell_format: The cell format
        :type cell_format: str
        """
        try:
            cell = row[column]
        except IndexError:
            cell = ''

        width = self._column_widths[column]
        if isinstance(cell, TableCell) and cell.colspan > 1:
            # add the width of the following columns(numbers of colspan).
            for next_column in range(column + 1, column + cell.colspan):
                width += self._get_column_separator_width() + self._column_widths[next_column]

        # Encoding fix
        width += len(cell) - Helper.len(cell)

        style = self.get_column_style(column)

        if isinstance(cell, TableSeparator):
            self._output.write(style.border_format % (style.horizontal_border_char * width))
        else:
            width += Helper.len(cell) - Helper.len_without_decoration(self._output.get_formatter(), cell)
            content = style.cell_row_content_format % cell
            self._output.write(cell_format % getattr(content, style.pad_type)(width, style.padding_char))

    def _calculate_number_of_columns(self):
        """
        Calculate number of columns for this table.
        """
        if self._number_of_columns is not None:
            return

        columns = [0]
        for row in self._headers + self._rows:
            if isinstance(row, TableSeparator):
                continue

            columns.append(self._get_number_of_columns(row))

        self._number_of_columns = max(columns)

    def _build_table_rows(self, rows):
        unmerged_rows = OrderedDict()

        row_key = 0
        while row_key < len(rows):
            rows = self._fill_next_rows(rows, row_key)

            # Remove any new line breaks and replace it with a new line
            for column, cell in enumerate(rows[row_key]):
                if '\n' not in cell:
                    continue

                lines = cell.split('\n')
                for line_key, line in enumerate(lines):
                    if isinstance(cell, TableCell):
                        line = TableCell(line, colspan=cell.colspan)

                    if 0 == line_key:
                        rows[row_key][column] = line
                    else:
                        if row_key not in unmerged_rows:
                            unmerged_rows[row_key] = OrderedDict()

                        if line_key not in unmerged_rows[row_key]:
                            unmerged_rows[row_key][line_key] = OrderedDict()

                        unmerged_rows[row_key][line_key][column] = line

            row_key += 1

        table_rows = []

        for row_key, row in enumerate(rows):
            table_rows.append(self._fill_cells(row))

            if row_key in unmerged_rows:
                for line in unmerged_rows[row_key]:
                    if line <= len(table_rows):
                        new_row = []
                        for column, value in enumerate(row):
                            if column in unmerged_rows[row_key][line]:
                                new_row.append(unmerged_rows[row_key][line][column])
                            else:
                                new_row.append('')

                        table_rows.append(new_row)
                    else:
                        for column in unmerged_rows[row_key][line]:
                            table_rows[line][column] = unmerged_rows[row_key][line][column]

        return table_rows

    def _fill_next_rows(self, rows, line):
        """
        Fill rows that contains rowspan > 1.

        :param rows: The rows to fill
        :type rows: list

        :type line: int

        :rtype: list
        """
        unmerged_rows = OrderedDict()

        for column, cell in enumerate(rows[line]):
            if isinstance(cell, TableCell) and cell.rowspan > 1:
                nb_lines = cell.rowspan - 1
                lines = [cell]

                if '\n' in cell:
                    lines = cell.split('\n')
                    if len(lines) > nb_lines:
                        nb_lines = cell.count('\n')

                    rows[line][column] = TableCell(lines[0], colspan=cell.colspan)

                # Create a two dimensional array (rowspan x colspan)
                placeholder = OrderedDict([(k, OrderedDict()) for k in range(line + 1, line + 1 + nb_lines)])
                for k, v in unmerged_rows.items():
                    if k in placeholder:
                        for l, m in unmerged_rows[k].items():
                            if l in placeholder[k]:
                                placeholder[k][l].update(m)
                            else:
                                placeholder[k][l] = m
                    else:
                        placeholder[k] = v

                unmerged_rows = placeholder

                for unmerged_row_key, unmerged_row in unmerged_rows.items():
                    value = ''
                    if unmerged_row_key - line < len(lines):
                        value = lines[unmerged_row_key - line]

                    unmerged_rows[unmerged_row_key][column] = TableCell(value, colspan=cell.colspan)

        for unmerged_row_key, unmerged_row in unmerged_rows.items():
            # we need to know if unmerged_row will be merged or inserted into rows
            if (unmerged_row_key < len(rows)
                and isinstance(rows[unmerged_row_key], list)
                and (self._get_number_of_columns(rows[unmerged_row_key])
                     + self._get_number_of_columns(list(unmerged_rows[unmerged_row_key].values()))
                        <= self._number_of_columns)):
                # insert cell into row at cell_key position
                for cell_key, cell in unmerged_row.items():
                    rows[unmerged_row_key].insert(cell_key, cell)
            else:
                row = self._copy_row(rows, unmerged_row_key - 1)
                for column, cell in unmerged_row.items():
                    if len(cell):
                        row[column] = unmerged_row[column]

                rows.insert(unmerged_row_key, row)

        return rows

    def _fill_cells(self, row):
        """
        Fill cells for a row that contains colspan > 1.

        :type row: list

        :rtype: list
        """
        new_row = []

        for column, cell in enumerate(row):
            new_row.append(cell)

            if isinstance(cell, TableCell) and cell.colspan > 1:
                for position in range(column + 1, column + cell.colspan):
                    # insert empty value at column position
                    new_row.append('')

        if new_row:
            return new_row

        return row

    def _copy_row(self, rows, line):
        """
        Copy a row

        :type rows: list

        :type line: int

        :rtype: list
        """
        row = [x for x in rows[line]]

        for cell_key, cell_value in enumerate(row):
            row[cell_key] = ''
            if isinstance(cell_value, TableCell):
                row[cell_key] = TableCell('', colspan=cell_value.colspan)

        return row

    def _get_number_of_columns(self, row):
        """
        Gets number of columns by row.

        :param row: The row
        :type row: list

        :rtype: int
        """
        columns = len(row)
        for column in row:
            if isinstance(column, TableCell):
                columns += column.colspan - 1

        return columns

    def _get_row_columns(self, row):
        """
        Gets list of columns for the given row.

        :type row: list

        :rtype: list
        """
        columns = list(range(0, self._number_of_columns))

        for cell_key, cell in enumerate(row):
            if isinstance(cell, TableCell) and cell.colspan > 1:
                # exclude grouped columns.
                columns = [x for x in columns if x not in list(range(cell_key + 1, cell_key + cell.colspan))]

        return columns

    def _calculate_columns_width(self, rows):
        """
        Calculates columns widths.
        """
        for column in range(0, self._number_of_columns):
            lengths = []
            for row in rows:
                if isinstance(row, TableSeparator):
                    continue

                lengths.append(self._get_cell_width(row, column))

            self._column_widths[column] = max(lengths) + len(self._style.cell_row_content_format) - 2

    def _get_column_separator_width(self):
        return len(self._style.border_format % self._style.vertical_border_char)

    def _get_cell_width(self, row, column):
        """
        Gets cell width.

        :type row: list

        :type column: int

        :rtype: int
        """
        try:
            cell = row[column]
            cell_width = Helper.len_without_decoration(self._output.get_formatter(), cell)

            if isinstance(cell, TableCell) and cell.colspan > 1:
                # we assume that cell value will be across more than one column.
                cell_width = cell_width // cell.colspan

            return cell_width

        except IndexError:
            return 0

    def _cleanup(self):
        self._column_widths = {}
        self._number_of_columns = None

    @classmethod
    def _init_styles(cls):
        borderless = TableStyle()
        borderless.set_horizontal_border_char('=')
        borderless.set_vertical_border_char(' ')
        borderless.set_crossing_char(' ')

        compact = TableStyle()
        compact.set_horizontal_border_char('')
        compact.set_vertical_border_char(' ')
        compact.set_crossing_char('')
        compact.set_cell_row_content_format('%s')

        return {
            'default': TableStyle(),
            'borderless': borderless,
            'compact': compact
        }


