from __future__ import annotations

import sys

from cleo.parser.common import _UNRECOGNIZED_ARGS_ATTR
from cleo.parser.common import SUPPRESS
from cleo.parser.common import NArgsEnum
from cleo.parser.common import _copy_items
from cleo.parser.deprecated import _AttributeHolder
from cleo.parser.exceptions import ArgumentError


class Action(_AttributeHolder):
    """Information about how to convert command line strings to Python objects.

    Action objects are used by an ArgumentParser to represent the information
    needed to parse a single argument from one or more strings from the
    command line. The keyword arguments to the Action constructor are also
    all attributes of Action instances.

    Keyword Arguments:

        - option_strings -- A list of command-line option strings which
            should be associated with this action.

        - dest -- The name of the attribute to hold the created object(s)

        - nargs -- The number of command-line arguments that should be
            consumed. By default, one argument will be consumed and a single
            value will be produced.  Other values include:
                - N (an integer) consumes N arguments (and produces a list)
                - '?' consumes zero or one arguments
                - '*' consumes zero or more arguments (and produces a list)
                - '+' consumes one or more arguments (and produces a list)
            Note that the difference between the default and nargs=1 is that
            with the default, a single value will be produced, while with
            nargs=1, a list containing a single value will be produced.

        - const -- The value to be produced if the option is specified and the
            option uses an action that takes no values.

        - default -- The value to be produced if the option is not specified.

        - type -- A callable that accepts a single string argument, and
            returns the converted value.  The standard Python types str, int,
            float, and complex are useful examples of such callables.  If None,
            str is used.

        - choices -- A container of values that should be allowed. If not None,
            after a command-line argument has been converted to the appropriate
            type, an exception will be raised if it is not a member of this
            collection.

        - required -- True if the action must always be specified at the
            command line. This is only meaningful for optional command-line
            arguments.

        - help -- The help string describing the argument.

        - metavar -- The name to be used for the option's argument with the
            help string. If None, the 'dest' value will be used as the name.
    """

    def __init__(
        self,
        option_strings,
        dest,
        nargs=None,
        const=None,
        default=None,
        type=None,
        choices=None,
        required=False,
        help=None,
        metavar=None,
        deprecated=False,
    ):
        self.option_strings = option_strings
        self.dest = dest
        self.nargs = nargs
        self.const = const
        self.default = default
        self.type = type
        self.choices = choices
        self.required = required
        self.help = help
        self.metavar = metavar
        self.deprecated = deprecated

    def _get_kwargs(self):
        names = [
            "option_strings",
            "dest",
            "nargs",
            "const",
            "default",
            "type",
            "choices",
            "required",
            "help",
            "metavar",
            "deprecated",
        ]
        return [(name, getattr(self, name)) for name in names]

    def format_usage(self):
        return self.option_strings[0]

    def __call__(self, parser, namespace, values, option_string=None):
        raise NotImplementedError(".__call__() not defined")


class BooleanOptionalAction(Action):
    def __init__(
        self,
        option_strings,
        dest,
        default=None,
        required=False,
        help=None,
        deprecated=False,
        **kwargs,
    ):
        _option_strings = []
        for option_string in option_strings:
            _option_strings.append(option_string)

            if option_string.startswith("--"):
                option_string = "--no-" + option_string[2:]
                _option_strings.append(option_string)

        super().__init__(
            option_strings=_option_strings,
            dest=dest,
            nargs=0,
            default=default,
            type=None,
            choices=None,
            required=required,
            help=help,
            metavar=None,
            deprecated=deprecated,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        if option_string in self.option_strings:
            setattr(namespace, self.dest, not option_string.startswith("--no-"))

    def format_usage(self):
        return " | ".join(self.option_strings)


class _StoreAction(Action):
    def __init__(
        self,
        option_strings,
        dest,
        nargs=None,
        const=None,
        default=None,
        type=None,
        choices=None,
        required=False,
        help=None,
        metavar=None,
        deprecated=False,
    ):
        if nargs == 0:
            raise ValueError(
                "nargs for store actions must be != 0; if you "
                "have nothing to store, actions such as store "
                "true or store const may be more appropriate"
            )
        if const is not None and nargs != NArgsEnum.OPTIONAL:
            raise ValueError("nargs must be %r to supply const" % NArgsEnum.OPTIONAL)
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            const=const,
            default=default,
            type=type,
            choices=choices,
            required=required,
            help=help,
            metavar=metavar,
            deprecated=deprecated,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


class _StoreConstAction(Action):
    def __init__(
        self,
        option_strings,
        dest,
        const=None,
        default=None,
        required=False,
        help=None,
        metavar=None,
        deprecated=False,
    ):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            const=const,
            default=default,
            required=required,
            help=help,
            deprecated=deprecated,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.const)


class _StoreTrueAction(_StoreConstAction):
    def __init__(
        self,
        option_strings,
        dest,
        default=False,
        required=False,
        help=None,
        deprecated=False,
    ):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            const=True,
            deprecated=deprecated,
            required=required,
            help=help,
            default=default,
        )


class _StoreFalseAction(_StoreConstAction):
    def __init__(
        self,
        option_strings,
        dest,
        default=True,
        required=False,
        help=None,
        deprecated=False,
    ):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            const=False,
            default=default,
            required=required,
            help=help,
            deprecated=deprecated,
        )


class _AppendAction(Action):
    def __init__(
        self,
        option_strings,
        dest,
        nargs=None,
        const=None,
        default=None,
        type=None,
        choices=None,
        required=False,
        help=None,
        metavar=None,
        deprecated=False,
    ):
        if nargs == 0:
            raise ValueError(
                "nargs for append actions must be != 0; if arg "
                "strings are not supplying the value to append, "
                "the append const action may be more appropriate"
            )
        if const is not None and nargs != NArgsEnum.OPTIONAL:
            raise ValueError("nargs must be %r to supply const" % NArgsEnum.OPTIONAL)
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            const=const,
            default=default,
            type=type,
            choices=choices,
            required=required,
            help=help,
            metavar=metavar,
            deprecated=deprecated,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest, None)
        items = _copy_items(items)
        items.append(values)
        setattr(namespace, self.dest, items)


class _AppendConstAction(Action):
    def __init__(
        self,
        option_strings,
        dest,
        const=None,
        default=None,
        required=False,
        help=None,
        metavar=None,
        deprecated=False,
    ):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            const=const,
            default=default,
            required=required,
            help=help,
            metavar=metavar,
            deprecated=deprecated,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest, None)
        items = _copy_items(items)
        items.append(self.const)
        setattr(namespace, self.dest, items)


class _CountAction(Action):
    def __init__(
        self,
        option_strings,
        dest,
        default=None,
        required=False,
        help=None,
        deprecated=False,
    ):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            default=default,
            required=required,
            help=help,
            deprecated=deprecated,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        count = getattr(namespace, self.dest, None)
        if count is None:
            count = 0
        setattr(namespace, self.dest, count + 1)


class _HelpAction(Action):
    def __init__(
        self,
        option_strings,
        dest=SUPPRESS,
        default=SUPPRESS,
        help=None,
        deprecated=False,
    ):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help,
            deprecated=deprecated,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        parser.exit()


class _VersionAction(Action):
    def __init__(
        self,
        option_strings,
        version=None,
        dest=SUPPRESS,
        default=SUPPRESS,
        help="show program's version number and exit",
        deprecated=False,
    ):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help,
        )
        self.version = version

    def __call__(self, parser, namespace, values, option_string=None):
        version = self.version
        if version is None:
            version = parser.version
        formatter = parser._get_formatter()
        formatter.add_text(version)
        parser._print_message(formatter.format_help(), sys.stdout)
        parser.exit()


class _SubParsersAction(Action):
    class _ChoicesPseudoAction(Action):
        def __init__(self, name, aliases, help):
            metavar = dest = name
            if aliases:
                metavar += " (%s)" % ", ".join(aliases)
            super(_SubParsersAction._ChoicesPseudoAction, self).__init__(
                option_strings=[], dest=dest, help=help, metavar=metavar
            )

    def __init__(
        self,
        option_strings,
        prog,
        parser_class,
        dest=SUPPRESS,
        required=False,
        help=None,
        metavar=None,
    ):
        self._prog_prefix = prog
        self._parser_class = parser_class
        self._name_parser_map = {}
        self._choices_actions = []
        self._deprecated = set()

        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=NArgsEnum.PARSER,
            choices=self._name_parser_map,
            required=required,
            help=help,
            metavar=metavar,
        )

    def add_parser(self, name, *, deprecated=False, **kwargs):
        # set prog from the existing prefix
        if kwargs.get("prog") is None:
            kwargs["prog"] = f"{self._prog_prefix} {name}"

        aliases = kwargs.pop("aliases", ())

        if name in self._name_parser_map:
            raise ArgumentError(self, "conflicting subparser: %s" % name)
        for alias in aliases:
            if alias in self._name_parser_map:
                raise ArgumentError(self, "conflicting subparser alias: %s" % alias)

        # create a pseudo-action to hold the choice help
        if "help" in kwargs:
            help = kwargs.pop("help")
            choice_action = self._ChoicesPseudoAction(name, aliases, help)
            self._choices_actions.append(choice_action)

        # create the parser and add it to the map
        parser = self._parser_class(**kwargs)
        self._name_parser_map[name] = parser

        # make parser available under aliases also
        for alias in aliases:
            self._name_parser_map[alias] = parser

        if deprecated:
            self._deprecated.add(name)
            self._deprecated.update(aliases)

        return parser

    def _get_subactions(self):
        return self._choices_actions

    def __call__(self, parser, namespace, values, option_string=None):
        parser_name = values[0]
        arg_strings = values[1:]

        # set the parser name if requested
        if self.dest is not SUPPRESS:
            setattr(namespace, self.dest, parser_name)

        # select the parser
        try:
            subparser = self._name_parser_map[parser_name]
        except KeyError as err:
            msg = f"unknown parser {parser_name!r} (choices: {', '.join(self._name_parser_map)!s})"
            raise ArgumentError(self, msg) from err

        if parser_name in self._deprecated:
            parser._warning(f"command '{parser_name!s}' is deprecated")

        # parse all the remaining options into the namespace
        # store any unrecognized options on the object, so that the top
        # level parser can decide what to do with them

        # In case this subparser defines new defaults, we parse them
        # in a new namespace object and then update the original
        # namespace for the relevant parts.
        subnamespace, arg_strings = subparser.parse_known_args(arg_strings, None)
        for key, value in vars(subnamespace).items():
            setattr(namespace, key, value)

        if arg_strings:
            vars(namespace).setdefault(_UNRECOGNIZED_ARGS_ATTR, [])
            getattr(namespace, _UNRECOGNIZED_ARGS_ATTR).extend(arg_strings)


class _ExtendAction(_AppendAction):
    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest, None)
        items = _copy_items(items)
        items.extend(values)
        setattr(namespace, self.dest, items)
