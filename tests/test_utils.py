from cleo._utils import format_time
import pytest


@pytest.mark.parametrize("input_secs,expected", [
    (0.1, "< 1 sec"),
    (1.0, "1 sec"),
    (2.0, "2 secs"),
    (59.0, "59 secs"),
    (60.0, "1 min"),
    (120.0, "2 mins"),
])
def test_format_time(input_secs: float, expected: str) -> None:
    assert format_time(input_secs) == expected
