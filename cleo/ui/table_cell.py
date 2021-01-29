from typing import Optional

from .table_cell_style import TableCellStyle


class TableCell(str):
    def __new__(
        cls,
        value: str = "",
        rowspan: int = 1,
        colspan: int = 1,
        style: Optional[TableCellStyle] = None,
    ) -> "TableCell":
        return super().__new__(cls, value)

    def __init__(
        self,
        value: str = "",
        rowspan: int = 1,
        colspan: int = 1,
        style: Optional[TableCellStyle] = None,
    ) -> None:
        self._rowspan = rowspan
        self._colspan = colspan
        self._style = style

    @property
    def rowspan(self) -> int:
        return self._rowspan

    @property
    def colspan(self) -> int:
        return self._colspan

    @property
    def style(self) -> Optional[TableCellStyle]:
        return self._style
