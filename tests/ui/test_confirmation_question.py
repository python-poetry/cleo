from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from cleo.ui.confirmation_question import ConfirmationQuestion


if TYPE_CHECKING:
    from cleo.io.buffered_io import BufferedIO


@pytest.mark.parametrize(
    ("input", "expected", "default"),
    [
        ("", True, True),
        ("", False, False),
        ("y", True, True),
        ("yes", True, True),
        ("n", False, True),
        ("no", False, True),
    ],
)
def test_ask(io: BufferedIO, input: str, expected: bool, default: bool) -> None:
    io.set_user_input(f"{input}\n")
    question = ConfirmationQuestion("Do you like French fries?", default)
    assert question.ask(io) == expected


def test_ask_with_custom_answer(io: BufferedIO) -> None:
    io.set_user_input("j\ny\n")

    question = ConfirmationQuestion("Do you like French fries?", False, r"(?i)^(j|y)")
    assert question.ask(io)

    question = ConfirmationQuestion("Do you like French fries?", False, r"(?i)^(j|y)")
    assert question.ask(io)
