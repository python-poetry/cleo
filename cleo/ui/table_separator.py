from __future__ import annotations

from .table_cell import TableCell


class TableSeparator(TableCell):
    def __init__(self) -> None:
        super().__init__("")
