import os
import subprocess

import pytest

from cleo.ui.question import Question


def has_tty_available():
    devnull = open(os.devnull, "w")
    exit_code = subprocess.call(["stty", "2"], stdout=devnull, stderr=devnull)

    return exit_code == 0


TTY_AVAILABLE = has_tty_available()


def test_ask(io):
    question = Question("What time is it?", "2PM")
    io.set_user_input("\n8AM\n")

    assert "2PM" == question.ask(io)

    io.clear_error()

    assert "8AM" == question.ask(io)
    assert "What time is it? " == io.fetch_error()


@pytest.mark.skipif(
    not TTY_AVAILABLE, reason="`stty` is required to test hidden response functionality"
)
def test_ask_hidden_response(io):
    question = Question("What time is it?", "2PM")
    question.hide()
    io.set_user_input("8AM\n")

    assert "8AM" == question.ask(io)
    assert "What time is it? " == io.fetch_error()


def test_ask_and_validate(io):
    error = "This is not a color!"

    def validator(color):
        if color not in ["white", "black"]:
            raise Exception(error)

        return color

    question = Question("What color was the white horse of Henry IV?", "white")
    question.set_validator(validator)
    question.set_max_attempts(2)

    io.set_user_input("\nblack\n")
    assert "white" == question.ask(io)
    assert "black" == question.ask(io)

    io.set_user_input("green\nyellow\norange\n")

    with pytest.raises(Exception) as e:
        question.ask(io)

    assert error == str(e.value)


def test_no_interaction(io):
    io.interactive(False)

    question = Question("Do you have a job?", "not yet")
    assert "not yet" == question.ask(io)


def test_ask_question_with_special_characters(io):
    question = Question("What time is it, Sébastien?", "2PMë")
    io.set_user_input("\n")

    assert "2PMë" == question.ask(io)
    assert "What time is it, Sébastien? " == io.fetch_error()
