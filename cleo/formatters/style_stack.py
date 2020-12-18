from typing import Optional

from cleo.exceptions import ValueException

from .style import Style


class StyleStack:
    def __init__(self, empty_style: Optional[Style] = None):
        if empty_style is None:
            empty_style = Style()

        self._empty_style = empty_style
        self._styles = []

    @property
    def current(self) -> Style:
        if not self._styles:
            return self._empty_style

        return self._styles[-1]

    def reset(self) -> None:
        self._styles = []

    def push(self, style: Style) -> None:
        self._styles.append(style)

    def pop(self, style: Optional[Style] = None) -> Style:
        if not self._styles:
            return self._empty_style

        if style is None:
            return self._styles.pop()

        for i, stacked_style in reversed(list(enumerate(self._styles))):
            if style.apply("") == stacked_style.apply(""):
                self._styles = self._styles[:i]

                return stacked_style

        raise ValueException("Invalid nested tag found")
