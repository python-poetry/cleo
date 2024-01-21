from __future__ import annotations

import operator

from functools import reduce
from pathlib import Path
from typing import TYPE_CHECKING
from typing import ClassVar


if TYPE_CHECKING:
    import inspect

    from types import FrameType


class Frame:
    _content_cache: ClassVar[dict[str, str]] = {}

    def __init__(self, frame_info: inspect.FrameInfo) -> None:
        self._frame = frame_info.frame
        self._frame_info = frame_info
        self._lineno = frame_info.lineno
        self._filename = frame_info.filename
        self._function = frame_info.function
        self._lines = None
        self._file_content: str | None = None

    @property
    def frame(self) -> FrameType:
        return self._frame

    @property
    def lineno(self) -> int:
        return self._lineno

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def function(self) -> str:
        return self._function

    @property
    def line(self) -> str:
        if not self._frame_info.code_context:
            return ""

        return self._frame_info.code_context[0]

    @property
    def _key(self) -> tuple[str, str, int]:
        return self._filename, self._function, self._lineno

    @property
    def file_content(self) -> str:
        if self._file_content is not None:
            return self._file_content
        if not self._filename:
            self._file_content = ""
            return ""
        if self._filename not in type(self)._content_cache:
            try:
                file_content = Path(self._filename).read_text(encoding="utf-8")
            except OSError:
                file_content = ""
            type(self)._content_cache[self._filename] = file_content
        self._file_content = type(self)._content_cache[self._filename]
        return self._file_content

    def __hash__(self) -> int:
        return reduce(operator.xor, map(hash, self._key))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Frame):
            return NotImplemented
        return self._key == other._key

    def __repr__(self) -> str:
        return f"<Frame {self._filename}, {self._function}, {self._lineno}>"
