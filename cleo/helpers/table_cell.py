# -*- coding: utf-8 -*-


class TableCell(str):
    """
    Represents a table cell
    """

    _options = {
        'rowspan': 1,
        "colspan": 1
    }

    def __new__(cls, value = '', **options):
        self = super(TableCell, cls).__new__(cls, value)

        return self

    def __init__(self, value, **options):
        super(TableCell, self).__init__()

        for key in self._options:
            if key not in options:
                options[key] = self._options[key]

        self.options = options

    @property
    def colspan(self):
        return self.options['colspan']

    @property
    def rowspan(self):
        return self.options['rowspan']
