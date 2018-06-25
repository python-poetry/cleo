# -*- coding: utf-8 -*-

import sys
import traceback
import os
import re

from io import UnsupportedOperation
from pylev import levenshtein
from collections import OrderedDict
from .outputs.output import Output
from .outputs.console_output import ConsoleOutput
from .inputs.argv_input import ArgvInput
from .inputs.list_input import ListInput
from .inputs.input_argument import InputArgument
from .inputs.input_option import InputOption
from .inputs.input_definition import InputDefinition
from .commands.command import Command
from .commands.help_command import HelpCommand
from .commands.list_command import ListCommand
from .commands.completions_command import CompletionsCommand
from .helpers import HelperSet, FormatterHelper, QuestionHelper
from .terminal import Terminal
from .exceptions import (
    CleoException,
    CommandNotFound, AmbiguousCommand,
    NamespaceNotFound, AmbiguousNamespace
)


class Application(object):
    """
    An Application is the container for a collection of commands.

    This class is optimized for a standard CLI environment.

    Usage:
    >>> app = Application('myapp', '1.0 (stable)')
    >>> app.add(HelpCommand())
    >>> app.run()
    """

    def __init__(self, name='UNKNOWN', version='UNKNOWN', complete=True):
        """
        Constructor

        :param name: The name of the application
        :type name: basestring
        :param version: The version of the application
        :type version: basestring
        """
        self._name = name
        self._version = version
        self._catch_exceptions = True
        self._auto_exit = True
        self._commands = OrderedDict()
        self._default_command = 'list'
        self._definition = self.get_default_input_definition()
        self._want_helps = False
        self._helper_set = self.get_default_helper_set()
        self._terminal = Terminal()
        self._running_command = None
        self._complete = complete
        self._single_command = False

        for command in self.get_default_commands():
            self.add(command)

    @property
    def terminal(self):
        return self._terminal

    def run(self, input_=None, output_=None):
        """
        Runs the current application

        :param input_: An Input Instance
        :type input_: cleo.input.Input
        :param output_: An Output instance
        :type output_: Output

        :return: 0 if everything went fine, or an error code
        :rtype: int
        """
        if input_ is None:
            input_ = ArgvInput()

        if output_ is None:
            output_ = ConsoleOutput()

        self.configure_io(input_, output_)

        try:
            status_code = self.do_run(input_, output_)
        except KeyboardInterrupt as e:
            status_code = 1

            if output_.is_debug():
                # If we are in debug mode
                # Display the exception
                if isinstance(output_, ConsoleOutput):
                    self.render_exception(e, output_.get_error_output())
                else:
                    self.render_exception(e, output_)
        except Exception as e:
            if not self._catch_exceptions:
                raise

            if output_.is_quiet():
                output_.set_verbosity(Output.VERBOSITY_NORMAL)

            if isinstance(output_, ConsoleOutput):
                self.render_exception(e, output_.get_error_output())
            else:
                self.render_exception(e, output_)

            if isinstance(e, CleoException):
                status_code = e.code
            else:
                status_code = e.errno if hasattr(e, 'errno') else 1

            if status_code == 0:
                status_code = 1

        if self._auto_exit:
            if status_code is None:
                status_code = 0

            if status_code > 255:
                status_code = 255

            sys.exit(status_code)

        return status_code

    def do_run(self, input_, output_):
        """
        Runs the current application

        :param input_: An Input Instance
        :type input_: cleo.inputs.Input
        :param output_: An Output instance
        :type output_: Output

        :return: 0 if everything went fine, or an error code
        :rtype: int
        """
        if input_.has_parameter_option(['--version', '-V']):
            output_.writeln(self.get_long_version())

            return 0

        name = self.get_command_name(input_)

        if input_.has_parameter_option(['--help', '-h']):
            if not name:
                name = 'help'
                input_ = ListInput([('command', 'help')])
            else:
                self._want_helps = True

        if not name:
            name = self._default_command
            input_ = ListInput([('command', name)])

        # the command name MUST be the first element of the input
        command = None

        while command is None:
            try:
                command = self.find(name)
            except AmbiguousCommand as e:
                alternatives = e.alternatives

                if (not alternatives
                    or not input_.is_interactive()):
                        raise

                rest = ''
                if len(alternatives) > 2:
                    rest = ' and <info>{}</> more'.format(len(alternatives) - 2)

                commands = '<info>{}</>, <info>{}</>{}'.format(
                    alternatives[0], alternatives[1], rest
                )

                message = (
                    '\n<comment>Command "<info>{}</>" is ambiguous ({}).</>'
                    .format(e.name, commands)
                )

                output_.writeln(message)

                return 1

        self._running_command = command
        status_code = command.run(input_, output_)
        self._running_command = None

        return status_code

    def set_helper_set(self, helper_set):
        self._helper_set = helper_set

    def get_helper_set(self):
        return self._helper_set

    def set_definition(self, definition):
        self._definition = definition

    def get_definition(self):
        if self._single_command:
            input_definition = self._definition
            input_definition.set_arguments()

            return input_definition

        return self._definition

    def get_help(self):
        return self.get_long_version()

    def set_catch_exceptions(self, boolean):
        self._catch_exceptions = boolean

    def set_auto_exit(self, boolean):
        self._auto_exit = boolean

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_version(self):
        return self._version

    def set_version(self, version):
        self._version = version

    def get_long_version(self):
        if 'UNKNOWN' != self.get_name() and 'UNKNOWN' != self.get_version():
            return '%s <info>%s</info>' % (self.get_name(), self.get_version())

        return 'Console Tool'

    def register(self, name):
        return self.add(Command(name))

    def add_commands(self, commands):
        for command in commands:
            self.add(command)

    def add(self, command):
        """
        Adds a command object.

        If a command with the same name already exists, it will be overridden.

        :param command: A Command object or a dictionary defining the command
        :type command: Command or dict

        :return: The registered command
        :rtype: Command
        """
        command.set_application(self)

        if not command.is_enabled():
            command.set_application(None)

            return

        try:
            command.get_definition()
        except AttributeError:
            raise Exception(
                'Command class "%s" is not correctly initialized.'
                'You probably forgot to call the parent constructor.'
                % command.__class__.__name__
            )

        self._commands[command.get_name()] = command

        for alias in command.get_aliases():
            self._commands[alias] = command

        return command

    def get(self, name):
        if name not in self._commands:
            raise Exception('The command "%s" does not exist.' % name)

        command = self._commands[name]

        if self._want_helps:
            self._want_helps = False

            help_command = self.get('help')
            help_command.set_command(command)

            return help_command

        return command

    def has(self, name):
        return name in self._commands

    def get_namespaces(self):
        namespaces = []
        for command in self._commands.values():
            namespaces.append(self.extract_namespace(command.get_name()))

            for alias in command.get_aliases():
                namespaces.append(self.extract_namespace(alias))

        namespaces = [ns for ns in namespaces if ns]

        seen = set()

        return [ns for ns in namespaces if not (ns in seen or seen.add(ns))]

    def find_namespace(self, namespace):
        all_namespaces = self.get_namespaces()
        expr = re.sub('([^:]+|)', lambda m: re.escape(m.group(1)) + '[^:]*', namespace)
        namespaces = sorted([
            ns for ns in all_namespaces
            if re.findall('^%s' % expr, ns)
        ])

        if not namespaces:
            alternatives = self.find_alternatives(namespace, all_namespaces)

            raise NamespaceNotFound(namespace, alternatives)

        exact = namespace in namespaces
        if len(namespaces) > 1 and not exact:
            raise AmbiguousNamespace(namespace, namespaces)

        return namespace if exact else namespaces[0]

    def find(self, name):
        all_commands = list(self._commands.keys())
        expr = re.sub('([^:]+|)',
                      lambda m: re.escape(m.group(1)) + '[^:]*',
                      name)
        commands = sorted([
            x for x in all_commands
            if re.findall('^%s' % expr, x)
        ])

        filtered_commands = [
            c for c in commands
            if re.findall('^%s$' % expr, c)
        ]

        if not commands or len(filtered_commands) < 1:
            pos = name.find(':')
            if pos >= 0:
                # Check if a namespace exists and contains commands
                self.find_namespace(name[:pos])

            alternatives = self.find_alternatives(name, all_commands)

            raise CommandNotFound(name, alternatives)

        # Filter out aliases for commands which are already on the list
        if len(commands) > 1:
            command_list = self._commands

            def f(name_or_alias):
                command_name = command_list[name_or_alias].get_name()

                return command_name == name_or_alias or (command_name not in commands)

            commands = sorted([c for c in commands if f(c)])

        exact = name in commands
        if len(commands) > 1 and not exact:
            raise AmbiguousCommand(name, commands)

        return self.get(name if exact else commands[0])

    def all(self, namespace=None):
        if namespace is None:
            return self._commands

        commands = OrderedDict()
        for name, command in self._commands.items():
            if namespace == self.extract_namespace(name, namespace.count(':') + 1):
                commands[name] = command

        return commands

    @classmethod
    def get_abbreviations(cls, names):
        abbrevs = {}
        for name in names:
            l = len(name)
            while l > 0:
                abbrev = name[:l]
                if not abbrev in abbrevs:
                    abbrevs[abbrev] = [name]
                else:
                    abbrevs[abbrev].append(name)

                l -= 1

        for name in names:
            abbrevs[name] = [name]

        return abbrevs

    def render_exception(self, e, output_):
        tb = traceback.extract_tb(sys.exc_info()[2])

        title = '  [%s]  ' % e.__class__.__name__
        l = len(title)
        width = self._terminal.width
        if not width:
            width = sys.maxsize

        formatter = output_.get_formatter()
        lines = []
        for line in re.split('\r?\n', str(e)):
            for splitline in [line[x:x + (width - 4)]
                              for x in range(0, len(line), width - 4)]:
                line_length = len(
                    re.sub('\[[^m]*m',
                           '',
                           formatter.format(splitline))) + 4
                lines.append((splitline, line_length))

                l = max(line_length, l)

        messages = ['']
        empty_line = formatter.format('<error>%s</error>' % (' ' * l))
        messages.append(empty_line)
        messages.append(formatter.format('<error>%s%s</error>'
                                         % (title,
                                            ' ' * max(0, l - len(title)))))

        for line in lines:
            messages.append(
                formatter.format('<error>  %s  %s</error>'
                                 % (line[0], ' ' * (l - line[1])))
            )

        messages.append(empty_line)
        messages.append('')

        output_.writeln(messages, Output.OUTPUT_RAW)

        if Output.VERBOSITY_VERBOSE <= output_.get_verbosity():
            output_.writeln('<comment>Exception trace:</comment>')

            for exc_info in tb:
                file_ = exc_info[0]
                line_number = exc_info[1]
                function = exc_info[2]
                line = exc_info[3]

                output_.writeln(' <info>%s</info> in <fg=cyan>%s()</> '
                                'at line <info>%s</info>'
                                % (file_, function, line_number))
                output_.writeln('   %s' % line)

            output_.writeln('')

        if self._running_command is not None:
            output_.writeln('<info>%s</info>'
                            % self._running_command.get_synopsis())

            output_.writeln('')

    def configure_io(self, input_, output_):
        """
        Configures the input and output instances based on the user arguments and options.

        :param input_: An Input instance
        :type input_: Input
        :param output_: An Output instance
        :type output_: Output
        """
        if input_.has_parameter_option('--ansi'):
            output_.set_decorated(True)
        elif input_.has_parameter_option('--no-ansi'):
            output_.set_decorated(False)

        if input_.has_parameter_option(['--no-interaction', '-n']):
            input_.set_interactive(False)
        elif self.get_helper_set().has('question'):
            input_stream = self.get_helper_set().get('question').input_stream
            try:
                is_atty = hasattr(input_stream, 'fileno')

                if hasattr(input_stream, 'isatty'):
                    is_atty = is_atty and input_stream.isatty()
                else:
                    is_atty = is_atty and os.isatty(input_stream)

            except (UnsupportedOperation, TypeError):
                is_atty = False

            if not is_atty and os.getenv('SHELL_INTERACTIVE') is None:
                input_.set_interactive(False)

        if input_.has_parameter_option(['--quiet', '-q']):
            output_.set_verbosity(Output.VERBOSITY_QUIET)
        elif input_.has_parameter_option('-vvv')\
                or input_.has_parameter_option('--verbose=3')\
                or input_.get_parameter_option('--verbose') == "3":
            output_.set_verbosity(Output.VERBOSITY_DEBUG)
        elif input_.has_parameter_option('-vv')\
                or input_.has_parameter_option('--verbose=2')\
                or input_.get_parameter_option('--verbose') == "2":
            output_.set_verbosity(Output.VERBOSITY_VERY_VERBOSE)
        elif input_.has_parameter_option('-v')\
                or input_.has_parameter_option('--verbose=1')\
                or input_.get_parameter_option('--verbose') == "1"\
                or input_.get_parameter_option('--verbose', False) is not False:
            output_.set_verbosity(Output.VERBOSITY_VERBOSE)

    def get_command_name(self, input_):
        if self._single_command:
            return self._default_command

        return input_.get_first_argument()

    def get_default_input_definition(self):
        return InputDefinition([
            InputArgument('command', InputArgument.REQUIRED, 'The command to execute'),

            InputOption('--help', '-h', InputOption.VALUE_NONE, 'Display this help message'),
            InputOption('--quiet', '-q', InputOption.VALUE_NONE, 'Do not output any message'),
            InputOption(
                '--verbose', '-v|vv|vvv', InputOption.VALUE_OPTIONAL,
                'Increase the verbosity of messages: 1 for normal output, '
                '2 for more verbose output and 3 for debug'
            ),
            InputOption('--version', '-V', InputOption.VALUE_NONE, 'Display this application version'),
            InputOption('--ansi', '', InputOption.VALUE_NONE, 'Force ANSI output'),
            InputOption('--no-ansi', '', InputOption.VALUE_NONE, 'Disable ANSI output'),
            InputOption('--no-interaction', '-n', InputOption.VALUE_NONE, 'Do not ask any interactive question')
        ])

    def get_default_commands(self):
        commands = [HelpCommand(), ListCommand()]

        if self._complete:
            commands.append(CompletionsCommand())

        return commands

    def get_default_helper_set(self):
        return HelperSet([
            FormatterHelper(),
            QuestionHelper()
        ])

    def sort_commands(self, commands):
        """
        Sorts command in alphabetical order

        :param commands: A dict of commands
        :type commands: dict

        :return: A sorted list of commands
        """
        namespaced_commands = {}
        for name, command in commands.items():
            key = self.extract_namespace(name, 1)
            if not key:
                key = '_global'

            if key in namespaced_commands:
                namespaced_commands[key][name] = command
            else:
                namespaced_commands[key] = {name: command}

        for namespace, commands in namespaced_commands.items():
            namespaced_commands[namespace] = sorted(commands.items(), key=lambda x: x[0])

        namespaced_commands = sorted(namespaced_commands.items(), key=lambda x: x[0])

        return namespaced_commands

    def extract_namespace(self, name, limit=None):
        parts = name.split(':')
        parts.pop()

        return ':'.join(parts[:limit] if limit else parts)

    def find_alternatives(self, name, collection):
        """
        Finds alternatives of name in collection

        :param name: The string
        :type name: str
        :param collection: The collection
        :type collection: list

        :return: A sorted list of similar strings
        """
        threshold = 1e3
        alternatives = {}

        collection_parts = {}
        for item in collection:
            collection_parts[item] = item.split(':')

        for i, subname in enumerate(name.split(':')):
            for collection_name, parts in collection_parts.items():
                exists = collection_name in alternatives
                if i not in parts and exists:
                    alternatives[collection_name] += threshold
                    continue
                elif i not in parts:
                    continue

                lev = levenshtein(subname, parts[i])
                if lev <= (len(subname) / 3) or parts[i].find(subname) != -1:
                    if exists:
                        alternatives[collection_name] += lev
                    else:
                        alternatives[collection_name] = lev
                elif exists:
                    alternatives[collection_name] += threshold

        for item in collection:
            lev = levenshtein(name, item)
            if lev <= (len(name) / 3) or item.find(name) != -1:
                if item in alternatives:
                    alternatives[item] = alternatives[item] - lev
                else:
                    alternatives[item] = lev

        alts = []
        for alt, score in alternatives.items():
            if score < 2 * threshold:
                alts.append(alt)

        return alts

    def set_default_command(self, command_name, is_single_command=False):
        """
        Sets the default Command name.

        :param command_name: The Command name
        :type command_name: str

        :param is_single_command: Set to True if there is only one command in this application
        :type is_single_command: bool
        """
        self._default_command = command_name

        if is_single_command:
            # Ensure the command exists
            self.find(command_name)

            self._single_command = True

        return self
