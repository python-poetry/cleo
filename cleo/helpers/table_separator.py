# -*- coding: utf-8 -*-

from .table_cell import TableCell


class TableSeparator(TableCell):
    """
    Marks a row as being a separator.
    """

    def __init__(self, **options):
        super(TableSeparator, self).__init__('', **options)
