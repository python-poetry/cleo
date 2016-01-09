# -*- coding: utf-8 -*-

import re
import os
from .exceptions import CleoException
from .inputs.input_argument import InputArgument
from .inputs.input_option import InputOption


class Parser(object):

    @classmethod
    def parse(cls, expression):
        """
        Parse the given console command definition into a dict.

        :param expression: The expression to parse
        :type expression: str

        :rtype: dict
        """
        parsed = {
            'name': None,
            'arguments': [],
            'options': []
        }

        if not expression.strip():
            raise CleoException('Console command signature is empty.')

        expression = expression.replace(os.linesep, '')

        matches = re.match('[^\s]+', expression)

        if not matches:
            raise CleoException('Unable to determine command name from signature.')

        name = matches.group(0)
        parsed['name'] = name

        tokens = re.findall('\{\s*(.*?)\s*\}', expression)

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
            if not token.startswith('--'):
                arguments.append(cls._parse_argument(token))
            else:
                options.append(cls._parse_option(token))

        return {
            'arguments': arguments,
            'options': options
        }

    @classmethod
    def _parse_argument(cls, token):
        """
        Parse an argument expression.

        :param token: The argument expression
        :type token: str

        :rtype: InputArgument
        """
        description = None
        validator = None

        if ' : ' in token:
            token, description = tuple(token.split(' : ', 2))

            token = token.strip()

            description = description.strip()

        # Checking validator:
        matches = re.match('(.*)\((.*?)\)', token)
        if matches:
            token = matches.group(1).strip()
            validator = matches.group(2).strip()

        if token.endswith('?*'):
            return InputArgument(
                token.rstrip('?*'),
                InputArgument.IS_LIST,
                description
            )
        elif token.endswith('*'):
            return InputArgument(
                token.rstrip('*'),
                InputArgument.IS_LIST | InputArgument.REQUIRED,
                description
            )
        elif token.endswith('?'):
            return InputArgument(
                token.rstrip('?'),
                InputArgument.OPTIONAL,
                description
            )

        matches = re.match('(.+)\=(.+)', token)
        if matches:
            return InputArgument(
                matches.group(1),
                InputArgument.OPTIONAL,
                description,
                matches.group(2)
            )

        return InputArgument(token, InputArgument.REQUIRED, description,
                             validator=validator)

    @classmethod
    def _parse_option(cls, token):
        """
        Parse an option expression.

        :param token: The option expression
        :type token: str

        :rtype: InputOption
        """
        description = None
        validator = None

        if ' : ' in token:
            token, description = tuple(token.split(' : ', 2))

            token = token.strip()

            description = description.strip()

        # Checking validator:
        matches = re.match('(.*)\((.*?)\)', token)
        if matches:
            token = matches.group(1).strip()
            validator = matches.group(2).strip()

        shortcut = None

        matches = re.split('\s*\|\s*', token, 2)

        if len(matches) > 1:
            shortcut = matches[0].lstrip('-')
            token = matches[1]

        default = None
        mode = InputOption.VALUE_NONE

        if token.endswith('=*'):
            mode = InputOption.VALUE_REQUIRED | InputOption.VALUE_IS_LIST
            token = token.rstrip('=*')
        elif token.endswith('=?*'):
            mode = InputOption.VALUE_OPTIONAL | InputOption.VALUE_IS_LIST
            token = token.rstrip('=?*')
        elif token.endswith("=?"):
            mode = InputOption.VALUE_OPTIONAL
            token = token.rstrip('=?')
        elif token.endswith('='):
            mode = InputOption.VALUE_REQUIRED
            token = token.rstrip('=')

        matches = re.match('(.+)(\=[\?\*]*)(.+)', token)
        if matches:
            token = matches.group(1)
            operator = matches.group(2)
            default = matches.group(3)

            if operator == '=*':
                mode = InputOption.VALUE_REQUIRED | InputOption.VALUE_IS_LIST
            elif operator == '=?*':
                mode = InputOption.VALUE_OPTIONAL | InputOption.VALUE_IS_LIST
            elif operator == '=?':
                mode = InputOption.VALUE_OPTIONAL
            elif operator == '=':
                mode = InputOption.VALUE_REQUIRED

        return InputOption(token, shortcut, mode, description, default,
                           validator=validator)
