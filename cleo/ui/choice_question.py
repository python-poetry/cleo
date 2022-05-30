from __future__ import annotations

import re

from typing import TYPE_CHECKING
from typing import Any

from cleo.exceptions import ValueException
from cleo.ui.question import Question


if TYPE_CHECKING:
    from cleo.io.io import IO


class SelectChoiceValidator:
    def __init__(self, question: Question) -> None:
        """
        Constructor.
        """
        self._question = question
        self._values = question.choices

    def validate(self, selected: str | int) -> str | None:
        """
        Validate a choice.
        """
        # Collapse all spaces.
        if isinstance(selected, int):
            selected = str(selected)

        if selected is None:
            return None

        selected_choices = selected.replace(" ", "")

        if self._question.supports_multiple_choices():
            # Check for a separated comma values
            if not re.match("^[a-zA-Z0-9_-]+(?:,[a-zA-Z0-9_-]+)*$", selected_choices):
                raise ValueException(self._question.error_message.format(selected))

            selected_choices = selected_choices.split(",")
        else:
            selected_choices = [selected]

        multiselect_choices = []
        for value in selected_choices:
            results = []

            for key, choice in enumerate(self._values):
                if choice == value:
                    results.append(key)

            if len(results) > 1:
                raise ValueException(
                    "The provided answer is ambiguous. Value should be one of {}.".format(
                        " or ".join(str(r) for r in results)
                    )
                )

            try:
                result = self._values.index(value)
                result = self._values[result]
            except ValueError:
                try:
                    value = int(value)

                    if 0 <= value < len(self._values):
                        result = self._values[value]
                    else:
                        result = False
                except ValueError:
                    result = False

            if result is False:
                raise ValueException(self._question.error_message.format(value))

            multiselect_choices.append(result)

        if self._question.supports_multiple_choices():
            return multiselect_choices

        return multiselect_choices[0]


class ChoiceQuestion(Question):
    """
    Multiple choice question.
    """

    def __init__(
        self, question: str, choices: list[str], default: Any | None = None
    ) -> None:
        super().__init__(question, default)

        self._multi_select = False
        self._choices = choices
        self._validator = SelectChoiceValidator(self).validate
        self._autocomplete_values = choices
        self._prompt = " > "
        self._error_message = 'Value "{}" is invalid'

    @property
    def error_message(self) -> str:
        return self._error_message

    @property
    def choices(self) -> list[str]:
        return self._choices

    def supports_multiple_choices(self) -> bool:
        return self._multi_select

    def set_multi_select(self, multi_select: bool) -> None:
        self._multi_select = multi_select

    def set_error_message(self, message: str) -> None:
        self._error_message = message

    def _write_prompt(self, io: IO) -> None:
        """
        Outputs the question prompt.
        """
        message = self._question
        default = self._default

        if default is None:
            message = f"<question>{message}</question>: "
        elif self._multi_select:
            choices = self._choices
            default = default.split(",")

            for i, value in enumerate(default):
                default[i] = choices[int(value.strip())]

            message = "<question>{}</question> [<comment>{}</comment>]:".format(
                message, ", ".join(default)
            )
        else:
            choices = self._choices
            message = "<question>{}</question> [<comment>{}</comment>]:".format(
                message, choices[int(default)]
            )

        if len(self._choices) > 1:
            width = max(*map(len, [str(k) for k, _ in enumerate(self._choices)]))
        else:
            width = 1

        messages = [message]
        for key, value in enumerate(self._choices):
            messages.append(" [<comment>{:{}}</>] {}".format(key, width, value))

        io.write_error_line("\n".join(messages))

        message = self._prompt

        io.write_error(message)
