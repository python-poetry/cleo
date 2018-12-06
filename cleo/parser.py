import re
import os

from collections import namedtuple

from clikit.api.args.format import Argument
from clikit.api.args.format import Option


_argument = namedtuple("argument", "name flags description default")
_option = namedtuple("option", "long_name short_name flags description default")


class Parser(object):
    @classmethod
    def parse(cls, expression):
        """
        Parse the given console command definition into a dict.

        :param expression: The expression to parse
        :type expression: str

        :rtype: dict
        """
        parsed = {"name": None, "arguments": [], "options": []}

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
    def _parameters(cls, tokens):
        """
        Extract all of the parameters from the tokens.

        :param tokens: The tokens to extract the parameters from
        :type tokens: list

        :rtype: dict
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
    def _parse_argument(cls, token):
        """
        Parse an argument expression.

        :param token: The argument expression
        :type token: str

        :rtype: InputArgument
        """
        description = ""
        validator = None

        if " : " in token:
            token, description = tuple(token.split(" : ", 2))

            token = token.strip()

            description = description.strip()

        # Checking validator:
        matches = re.match(r"(.*)\((.*?)\)", token)
        if matches:
            token = matches.group(1).strip()
            validator = matches.group(2).strip()

        if token.endswith("?*"):
            return _argument(
                token.rstrip("?*"), Argument.MULTI_VALUED, description, None
            )
        elif token.endswith("*"):
            return _argument(
                token.rstrip("*"),
                Argument.MULTI_VALUED & Argument.REQUIRED,
                description,
                None,
            )
        elif token.endswith("?"):
            return _argument(token.rstrip("?"), Argument.OPTIONAL, description, None)

        matches = re.match(r"(.+)=(.+)", token)
        if matches:
            return _argument(
                matches.group(1), Argument.OPTIONAL, description, matches.group(2)
            )

        return _argument(token, Argument.REQUIRED, description, None)

    @classmethod
    def _parse_option(cls, token):
        """
        Parse an option expression.

        :param token: The option expression
        :type token: str

        :rtype: InputOption
        """
        description = ""
        validator = None

        if " : " in token:
            token, description = tuple(token.split(" : ", 2))

            token = token.strip()

            description = description.strip()

        # Checking validator:
        matches = re.match(r"(.*)\((.*?)\)", token)
        if matches:
            token = matches.group(1).strip()
            validator = matches.group(2).strip()

        shortcut = None

        matches = re.split(r"\s*\|\s*", token, 2)

        if len(matches) > 1:
            shortcut = matches[0].lstrip("-")
            token = matches[1]
        else:
            token = token.lstrip("-")

        default = None
        mode = Option.NO_VALUE

        if token.endswith("=*"):
            mode = Option.MULTI_VALUED
            token = token.rstrip("=*")
        elif token.endswith("=?*"):
            mode = Option.OPTIONAL_VALUE & Option.MULTI_VALUED
            token = token.rstrip("=?*")
        elif token.endswith("=?"):
            mode = Option.OPTIONAL_VALUE
            token = token.rstrip("=?")
        elif token.endswith("="):
            mode = Option.REQUIRED_VALUE
            token = token.rstrip("=")

        matches = re.match(r"(.+)(=[?*]*)(.+)", token)
        if matches:
            token = matches.group(1)
            operator = matches.group(2)
            default = matches.group(3)

            if operator == "=*":
                mode = Option.REQUIRED_VALUE & Option.MULTI_VALUED
            elif operator == "=?*":
                mode = Option.OPTIONAL_VALUE & Option.MULTI_VALUED
            elif operator == "=?":
                mode = Option.OPTIONAL_VALUE
            elif operator == "=":
                mode = Option.REQUIRED_VALUE

        return _option(token, shortcut, mode, description, default)
