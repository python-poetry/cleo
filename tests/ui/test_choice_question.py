from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from cleo.exceptions import CleoValueError
from cleo.ui.choice_question import ChoiceQuestion


if TYPE_CHECKING:
    from cleo.io.buffered_io import BufferedIO


def test_ask_choice(io: BufferedIO) -> None:
    io.set_user_input(
        "\n"
        "1\n"
        "  1  \n"
        "John\n"
        "1\n"
        "\n"
        "John\n"
        "1\n"
        "0,2\n"
        " 0 , 2  \n"
        "\n"
        "\n"
        "4\n"
        "0\n"
        "-2\n"
    )

    heroes = ["Superman", "Batman", "Spiderman"]
    question = ChoiceQuestion("What is your favorite superhero?", heroes, "2")
    question.set_max_attempts(1)

    # First answer is an empty answer, we're supposed to receive the default value
    assert question.ask(io) == "Spiderman"

    question = ChoiceQuestion("What is your favorite superhero?", heroes)
    question.set_max_attempts(1)

    assert question.ask(io) == "Batman"
    assert question.ask(io) == "Batman"

    question = ChoiceQuestion("What is your favorite superhero?", heroes)
    question.set_error_message('Input "{}" is not a superhero!')
    question.set_max_attempts(2)
    io.clear_error()

    assert question.ask(io) == "Batman"
    assert 'Input "John" is not a superhero!' in io.fetch_error()
    # Empty answer and no default is None
    assert question.ask(io) is None

    question = ChoiceQuestion("What is your favorite superhero?", heroes, "1")
    question.set_max_attempts(1)

    with pytest.raises(Exception) as e:
        question.ask(io)

    assert str(e.value) == 'Value "John" is invalid'

    question = ChoiceQuestion("What is your favorite superhero?", heroes)
    question.set_max_attempts(1)
    question.set_multi_select(True)

    assert question.ask(io) == ["Batman"]
    assert question.ask(io) == ["Superman", "Spiderman"]
    assert question.ask(io) == ["Superman", "Spiderman"]

    question = ChoiceQuestion("What is your favorite superhero?", heroes, "0,1")
    question.set_max_attempts(1)
    question.set_multi_select(True)

    assert question.ask(io) == ["Superman", "Batman"]

    question = ChoiceQuestion("What is your favorite superhero?", heroes, " 0 , 1 ")
    question.set_max_attempts(1)
    question.set_multi_select(True)

    assert question.ask(io) == ["Superman", "Batman"]

    question = ChoiceQuestion("What is your favourite superhero?", heroes)
    question.set_max_attempts(1)

    with pytest.raises(CleoValueError) as e:
        question.ask(io)

    assert str(e.value) == 'Value "4" is invalid'
    assert question.ask(io) == "Superman"

    with pytest.raises(CleoValueError) as e:
        question.ask(io)

    assert str(e.value) == 'Value "-2" is invalid'
