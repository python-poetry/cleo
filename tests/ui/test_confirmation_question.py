from cleo.ui.confirmation_question import ConfirmationQuestion


def test_ask(io):
    data = [
        ("", True),
        ("", False, False),
        ("y", True),
        ("yes", True),
        ("n", False),
        ("no", False),
    ]

    for d in data:
        io.set_user_input(d[0] + "\n")
        default = d[2] if len(d) > 2 else True
        question = ConfirmationQuestion("Do you like French fries?", default)
        assert d[1] == question.ask(io)


def test_ask_with_custom_answer(io):
    io.set_user_input("j\ny\n")

    question = ConfirmationQuestion("Do you like French fries?", False, "(?i)^(j|y)")
    assert question.ask(io)

    question = ConfirmationQuestion("Do you like French fries?", False, "(?i)^(j|y)")
    assert question.ask(io)
