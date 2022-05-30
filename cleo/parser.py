from __future__ import annotations

import os
import re

from typing import Any

from cleo.io.inputs.argument import Argument
from cleo.io.inputs.option import Option


class Parser:
    @classmethod
    def parse(cls, expression: str) -> dict[str, Any]:
        """
        Parse the given console command definition into a dict.
        """
        parsed: dict[str, Any] = {"name": None, "arguments": [], "options": []}

        if not expression.strip():
            raise ValueError("Console command signature is empty.")

        expression = expression.replace(os.linesep, "")

        matches = re.match(r"[^\s]+", expression)

        if not matches:
            raise ValueError("Unable to determine command name from signature.")

        name = matches.group(0)
        parsed["name"] = name

        tokens = re.findall(r"\{\s*(.*?)\s*\}", expression)

        if tokens:
            parsed.update(cls._parameters(tokens))

        return parsed

    @classmethod
    def _parameters(cls, tokens: list[str]) -> dict[str, Any]:
        """
        Extract all of the parameters from the tokens.
        """
        arguments = []
        options = []

        for token in tokens:
            if not token.startswith("--"):
                arguments.append(cls._parse_argument(token))
            else:
                options.append(cls._parse_option(token))

        return {"arguments": arguments, "options": options}

    @classmethod
    def _parse_argument(cls, token: str) -> Argument:
        """
        Parse an argument expression.
        """
        description = ""

        if " : " in token:
            token, description = tuple(token.split(" : ", 2))

            token = token.strip()

            description = description.strip()

        # Checking validator:
        matches = re.match(r"(.*)\((.*?)\)", token)
        if matches:
            token = matches.group(1).strip()

        if token.endswith("?*"):
            return Argument(
                token.rstrip("?*"),
                required=False,
                is_list=True,
                description=description,
            )
        elif token.endswith("*"):
            return Argument(
                token.rstrip("*"),
                is_list=True,
                description=description,
            )
        elif token.endswith("?"):
            return Argument(
                token.rstrip("?"),
                required=False,
                description=description,
            )

        matches = re.match(r"(.+)=(.+)", token)
        if matches:
            return Argument(
                matches.group(1),
                required=False,
                description=description,
                default=matches.group(2),
            )

        return Argument(
            token,
            description=description,
        )

    @classmethod
    def _parse_option(cls, token: str) -> Option:
        """
        Parse an option expression.
        """
        description = ""

        if " : " in token:
            token, description = tuple(token.split(" : ", 2))

            token = token.strip()

            description = description.strip()

        # Checking validator:
        matches = re.match(r"(.*)\((.*?)\)", token)
        if matches:
            token = matches.group(1).strip()

        shortcut = None

        matches = re.split(r"\s*\|\s*", token, 2)

        if len(matches) > 1:
            shortcut = matches[0].lstrip("-")
            token = matches[1]
        else:
            token = token.lstrip("-")

        default = None
        flag = True
        requires_value = False
        is_list = False

        if token.endswith("=*"):
            flag = False
            is_list = True
            requires_value = True
            token = token.rstrip("=*")
        elif token.endswith("=?*"):
            flag = False
            is_list = True
            token = token.rstrip("=?*")
        elif token.endswith("=?"):
            flag = False
            token = token.rstrip("=?")
        elif token.endswith("="):
            flag = False
            requires_value = True
            token = token.rstrip("=")
        else:
            matches = re.match(r"(.+)(=[?*]*)(.+)", token)
            if matches:
                flag = False
                token = matches.group(1)
                operator = matches.group(2)
                default = matches.group(3)

                if operator == "=*":
                    requires_value = True
                    is_list = True
                elif operator == "=?*":
                    is_list = True
                elif operator == "=?":
                    requires_value = False
                elif operator == "=":
                    requires_value = True

        return Option(
            token,
            shortcut,
            flag=flag,
            requires_value=requires_value,
            is_list=is_list,
            description=description,
            default=default,
        )
