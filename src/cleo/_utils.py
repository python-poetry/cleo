from __future__ import annotations

import math
import unicodedata

from dataclasses import dataclass
from difflib import SequenceMatcher
from functools import lru_cache
from html.parser import HTMLParser


class TagStripper(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)

        self.reset()
        self.fed: list[str] = []

    def handle_data(self, d: str) -> None:
        self.fed.append(d)

    def handle_entityref(self, name: str) -> None:
        self.fed.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.fed.append(f"&#{name};")

    def get_data(self) -> str:
        return "".join(self.fed)


def _strip(value: str) -> str:
    s = TagStripper()
    s.feed(value)
    s.close()

    return s.get_data()


def strip_tags(value: str) -> str:
    while "<" in value and ">" in value:
        new_value = _strip(value)
        if value.count("<") == new_value.count("<"):
            break

        value = new_value

    return value


def find_similar_names(name: str, names: list[str]) -> list[str]:
    """
    Finds names similar to a given command name.
    """
    threshold = 0.4
    distance_by_name = {}
    if " " in name:
        names = [name for name in names if " " in name]
    for actual_name in names:
        distance = SequenceMatcher(None, actual_name, name).ratio()

        is_similar = distance <= len(name) / 3
        substring_index = actual_name.find(name)
        is_substring = substring_index != -1

        if is_similar or is_substring:
            distance_by_name[actual_name] = (
                distance,
                substring_index if is_substring else float("inf"),
            )

    # Only keep results with a distance below the threshold
    distance_by_name = {
        key: value for key, value in distance_by_name.items() if value[0] > threshold
    }
    # Display results with shortest distance first
    return sorted(distance_by_name, key=lambda key: distance_by_name[key])


@dataclass
class TimeFormat:
    threshold: int
    alias: str
    divisor: int | None = None

    def apply(self, secs: float) -> str:
        if self.divisor:
            return f"{math.ceil(secs / self.divisor)} {self.alias}"
        return self.alias


_TIME_FORMATS: list[TimeFormat] = [
    TimeFormat(1, "< 1 sec"),
    TimeFormat(2, "1 sec"),
    TimeFormat(60, "secs", 1),
    TimeFormat(61, "1 min"),
    TimeFormat(3600, "mins", 60),
    TimeFormat(5401, "1 hr"),
    TimeFormat(86400, "hrs", 3600),
    TimeFormat(129601, "1 day"),
    TimeFormat(604801, "days", 86400),
]


def format_time(secs: float) -> str:
    time_format = next(
        (fmt for fmt in _TIME_FORMATS if secs < fmt.threshold), _TIME_FORMATS[-1]
    )
    return time_format.apply(secs)


@lru_cache(100)
def wcwidth(c: str) -> int:
    """Determine how many columns are needed to display a character in a terminal.

    Returns -1 if the character is not printable.
    Returns 0, 1 or 2 for other characters.
    """
    o = ord(c)

    # ASCII fast path.
    if 0x20 <= o < 0x07F:
        return 1

    # Some Cf/Zp/Zl characters which should be zero-width.
    if (
        o == 0x0000
        or 0x200B <= o <= 0x200F
        or 0x2028 <= o <= 0x202E
        or 0x2060 <= o <= 0x2063
    ):
        return 0

    category = unicodedata.category(c)

    # Control characters.
    if category == "Cc":
        return -1

    # Combining characters with zero width.
    if category in ("Me", "Mn"):
        return 0

    # Full/Wide east asian characters.
    if unicodedata.east_asian_width(c) in ("F", "W"):
        return 2

    return 1


def wcswidth(s: str) -> int:
    """Determine how many columns are needed to display a string in a terminal.

    Returns -1 if the string contains non-printable characters.
    """
    width = 0
    for c in unicodedata.normalize("NFC", s):
        wc = wcwidth(c)
        if wc < 0:
            return -1
        width += wc
    return width
