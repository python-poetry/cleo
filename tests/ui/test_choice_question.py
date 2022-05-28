import pytest

from cleo.exceptions import ValueError
from cleo.ui.choice_question import ChoiceQuestion


def test_ask_choice(io):
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
    assert "Spiderman" == question.ask(io)

    question = ChoiceQuestion("What is your favorite superhero?", heroes)
    question.set_max_attempts(1)

    assert "Batman" == question.ask(io)
    assert "Batman" == question.ask(io)

    question = ChoiceQuestion("What is your favorite superhero?", heroes)
    question.set_error_message('Input "{}" is not a superhero!')
    question.set_max_attempts(2)
    io.clear_error()

    assert "Batman" == question.ask(io)
    assert 'Input "John" is not a superhero!' in io.fetch_error()
    # Empty answer and no default is None
    assert question.ask(io) is None

    question = ChoiceQuestion("What is your favorite superhero?", heroes, "1")
    question.set_max_attempts(1)

    with pytest.raises(Exception) as e:
        question.ask(io)

    assert 'Value "John" is invalid' == str(e.value)

    question = ChoiceQuestion("What is your favorite superhero?", heroes)
    question.set_max_attempts(1)
    question.set_multi_select(True)

    assert ["Batman"] == question.ask(io)
    assert ["Superman", "Spiderman"] == question.ask(io)
    assert ["Superman", "Spiderman"] == question.ask(io)

    question = ChoiceQuestion("What is your favorite superhero?", heroes, "0,1")
    question.set_max_attempts(1)
    question.set_multi_select(True)

    assert ["Superman", "Batman"] == question.ask(io)

    question = ChoiceQuestion("What is your favorite superhero?", heroes, " 0 , 1 ")
    question.set_max_attempts(1)
    question.set_multi_select(True)

    assert ["Superman", "Batman"] == question.ask(io)

    question = ChoiceQuestion("What is your favourite superhero?", heroes)
    question.set_max_attempts(1)

    with pytest.raises(ValueError) as e:
        question.ask(io)

    assert 'Value "4" is invalid' == str(e.value)
    assert "Superman" == question.ask(io)

    with pytest.raises(ValueError) as e:
        question.ask(io)

    assert 'Value "-2" is invalid' == str(e.value)
