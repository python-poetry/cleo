from __future__ import annotations

import os
import subprocess

from typing import TYPE_CHECKING

import pytest

from cleo.ui.question import Question


if TYPE_CHECKING:
    from cleo.io.buffered_io import BufferedIO


def has_tty_available() -> bool:
    with open(os.devnull, "w") as devnull:
        exit_code = subprocess.call(["stty", "2"], stdout=devnull, stderr=devnull)

    return exit_code == 0


TTY_AVAILABLE = has_tty_available()


def test_ask(io: BufferedIO) -> None:
    question = Question("What time is it?", "2PM")
    io.set_user_input("\n8AM\n")

    assert question.ask(io) == "2PM"

    io.clear_error()

    assert question.ask(io) == "8AM"
    assert io.fetch_error() == "What time is it? "


@pytest.mark.skipif(
    not TTY_AVAILABLE, reason="`stty` is required to test hidden response functionality"
)
def test_ask_hidden_response(io: BufferedIO) -> None:
    question = Question("What time is it?", "2PM")
    question.hide()
    io.set_user_input("8AM\n")

    assert question.ask(io) == "8AM"
    assert io.fetch_error() == "What time is it? "


def test_ask_and_validate(io: BufferedIO) -> None:
    error = "This is not a color!"

    def validator(color: str) -> str:
        if color not in ["white", "black"]:
            raise Exception(error)

        return color

    question = Question("What color was the white horse of Henry IV?", "white")
    question.set_validator(validator)
    question.set_max_attempts(2)

    io.set_user_input("\nblack\n")
    assert question.ask(io) == "white"
    assert question.ask(io) == "black"

    io.set_user_input("green\nyellow\norange\n")

    with pytest.raises(Exception) as e:
        question.ask(io)

    assert str(e.value) == error


def test_no_interaction(io: BufferedIO) -> None:
    io.interactive(False)

    question = Question("Do you have a job?", "not yet")
    assert question.ask(io) == "not yet"


def test_ask_question_with_special_characters(io: BufferedIO) -> None:
    question = Question("What time is it, Sébastien?", "2PMë")
    io.set_user_input("\n")

    assert question.ask(io) == "2PMë"
    assert io.fetch_error() == "What time is it, Sébastien? "
