import os

from typing import List
from typing import Optional

from cleo.color import Color


class Style:
    def __init__(
        self,
        foreground: Optional[str] = None,
        background: Optional["str"] = None,
        options: Optional[List[str]] = None,
    ) -> None:
        self._foreground = foreground or ""
        self._background = background or ""
        self._options = options or []
        self._href = None
        self._supports_href = None

        self._color = Color(self._foreground, self._background, self._options)

    def foreground(self, foreground: str) -> "Style":
        self._color = Color(foreground, self._background, self._options)
        self._foreground = foreground

        return self

    def background(self, background: str) -> "Style":
        self._color = Color(self._foreground, background, self._options)
        self._background = background

        return self

    def bold(self, bold: bool = True) -> "Style":
        return self.set_option("bold") if bold else self.unset_option("bold")

    def dark(self, dark: bool = True) -> "Style":
        return self.set_option("dark") if dark else self.unset_option("dark")

    def underlines(self, underlined: bool = True) -> "Style":
        return (
            self.set_option("underline")
            if underlined
            else self.unset_option("underline")
        )

    def italic(self, italic: bool = True) -> "Style":
        return self.set_option("italic") if italic else self.unset_option("italic")

    def blinking(self, blinking: bool = True) -> "Style":
        return self.set_option("blink") if blinking else self.unset_option("blink")

    def inverse(self, inverse: bool = True) -> "Style":
        return self.set_option("reverse") if inverse else self.unset_option("reverse")

    def hidden(self, hidden: bool = True) -> "Style":
        return self.set_option("conceal") if hidden else self.unset_option("conceal")

    def href(self, uri: str) -> "Style":
        self._href = uri

        return self

    def set_option(self, option: str) -> "Style":
        self._options.append(option)
        self._color = Color(self._foreground, self._background, self._options)

        return self

    def unset_option(self, option: str) -> "Style":
        try:
            index = self._options.index(option)
        except IndexError:
            return self

        del self._options[index]

        self._color = Color(self._foreground, self._background, self._options)

    def apply(self, text: str) -> str:
        if self._supports_href is None:
            self._supports_href = os.getenv(
                "TERMINAL_EMULATOR"
            ) != "JetBrains-JediTerm" and (
                "KONSOLE_VERSION" not in os.environ
                or int(os.environ["KONSOLE_VERSION"]) > 201100
            )

        if self._href is not None and self._supports_href:
            text = f"\033]8;;{self._href}\033\\{text}\033]8;;\033\\"

        return self._color.apply(text)
