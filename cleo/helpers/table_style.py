# -*- coding: utf-8 -*-

from ..exceptions import CleoException


class TableStyle(object):

    padding_char = ' '
    horizontal_border_char = '-'
    vertical_border_char = '|'
    crossing_char = '+'
    cell_header_format = '<info>%s</info>'
    cell_row_format = '%s'
    cell_row_content_format = ' %s '
    border_format = '%s'
    pad_type = 'ljust'

    def set_padding_char(self, padding_char):
        if not padding_char:
            raise CleoException('Padding char must not be empty')

        self.padding_char = padding_char

        return self

    def set_horizontal_border_char(self, horizontal_border_char):
        self.horizontal_border_char = horizontal_border_char

        return self

    def set_vertical_border_char(self, vertical_border_char):
        self.vertical_border_char = vertical_border_char

        return self

    def set_crossing_char(self, crossing_char):
        self.crossing_char = crossing_char

        return self

    def set_cell_header_format(self, cell_header_format):
        self.cell_header_format = cell_header_format

        return self

    def set_cell_row_format(self, cell_row_format):
        self.cell_row_format = cell_row_format

        return self

    def set_cell_row_content_format(self, cell_row_content_format):
        self.cell_row_content_format = cell_row_content_format

        return self

    def set_border_format(self, border_format):
        self.border_format = border_format

        return self

    def set_pad_type(self, pad_type):
        pad_types = {
            'left': 'rjust',
            'right': 'ljust',
            'center': 'center'
        }

        if pad_type not in pad_types:
            raise CleoException('Invalid pad type. Must be either "left", "right" or "center".')

        self.pad_type = pad_types[pad_type]

        return self
