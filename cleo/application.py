# -*- coding: utf-8 -*-

import sys
import traceback
import os
import re
import termios
import fcntl
import struct
from io import UnsupportedOperation
from pylev import levenshtein

from .outputs.output import Output
from .outputs.console_output import ConsoleOutput, StreamOutput
from .inputs.argv_input import ArgvInput
from .inputs.list_input import ListInput
from .inputs.input_argument import InputArgument
from .inputs.input_option import InputOption
from .inputs.input_definition import InputDefinition
from .commands.command import Command
from .commands.help_command import HelpCommand
from .commands.list_command import ListCommand
from .helpers import HelperSet, FormatterHelper, DialogHelper, ProgressHelper


class Application(object):
    """
    An Application is the container for a collection of commands.

    This class is optimized for a standard CLI environment.

    Usage:
    >>> app = Application('myapp', '1.0 (stable)')
    >>> app.add(HelpCommand())
    >>> app.run()
    """

    def __init__(self, name='UNKNOWN', version='UNKNOWN'):
        """
        Constructor

        @param name: The name of the application
        @type name: basestring
        @param version: The version of the application
        @type version: basestring
        """
        self._name = name
        self._version = version
        self._catch_exceptions = True
        self._auto_exit = True
        self._commands = {}
        self._default_command = 'list'
        self._definition = self.get_default_input_definition()
        self._want_helps = False
        self._helper_set = self.get_default_helper_set()
        self._terminal_dimensions = ()
        self._running_command = None

        for command in self.get_default_commands():
            self.add(command)

    def run(self, input_=None, output_=None):
        """
        Runs the current application

        @param input_: An Input Instance
        @type input_: cleo.input.Input
        @param output_: An Output instance
        @type output_: Output

        @return: 0 if everything went fine, or an error code
        @rtype: int
        """
        if input_ is None:
            input_ = ArgvInput()

        if output_ is None:
            output_ = ConsoleOutput()

        self.configure_io(input_, output_)

        try:
            status_code = self.do_run(input_, output_)
        except Exception as e:
            if not self._catch_exceptions:
                raise

            if isinstance(output_, ConsoleOutput):
                self.render_exception(e, output_.get_error_output())
            else:
                self.render_exception(e, output_)

            status_code = e.errno if hasattr(e, 'errno') else 1

            if status_code == 0:
                status_code = 1

        if self._auto_exit:
            if status_code > 255:
                status_code = 255

            exit(status_code)

        return status_code

    def do_run(self, input_, output_):
        """
        Runs the current application

        @param input_: An Input Instance
        @type input_: cleo.inputs.Input
        @param output_: An Output instance
        @type output_: Output

        @return: 0 if everything went fine, or an error code
        @rtype: int
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
        command = self.find(name)
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
        return self._definition

    def get_help(self):
        messages = [
            self.get_long_version(),
            '',
            '<comment>Usage:</comment>',
            '  [options] command [arguments]',
            '',
            '<comment>Options:</comment>'
        ]

        for option in self.get_definition().get_options():
            messages.append('  %-29s %s %s'
                            % ('<info>--' + option.get_name() + '</info>',
                               '<info>-' + option.get_shortcut() + '</info>' if option.get_shortcut() else '  ',
                               option.get_description()))

        return '\n'.join(messages)

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
            return '<info>%s</info> version <comment>%s</comment>' % (self.get_name(), self.get_version())

        return '<info>Console Tool</info>'

    def register(self, name):
        return self.add(Command(name))

    def add_commands(self, commands):
        for command in commands:
            self.add(command)

    def add(self, command):
        """
        Adds a command object.

        If a command with the same name already exists, it will be overridden.

        @param command: A Command object
        @type command: Command

        @return: The registered command
        @rtype: Command
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

        return list(set(filter(lambda n: n, namespaces)))

    def find_namespace(self, namespace):
        all_namespaces = self.get_namespaces()
        expr = re.sub('([^:]+|)', lambda m: re.escape(m.group(1)) + '[^:]*', namespace)
        namespaces = sorted(
            list(
                filter(
                    lambda x: re.findall('^%s' % expr, x),
                    all_namespaces
                )
            )
        )

        if not namespaces:
            message = 'There are no commands defined in the "%s" namespace.' % namespace

            alternatives = self.find_alternatives(namespace, all_namespaces)
            if alternatives:
                if len(alternatives) == 1:
                    message += '\n\nDid you mean this?\n    '
                else:
                    message += '\n\nDid you mean one of these?\n    '

                message += '\n    '.join(alternatives)

            raise Exception(message)

        exact = namespace in namespaces
        if len(namespaces) > 1 and not exact:
            raise Exception('The namespace "%s" is ambiguous (%s).'
                            % (namespace,
                               self.get_abbreviation_suggestions(namespaces)))

        return namespace if exact else namespaces[0]

    def find(self, name):
        all_commands = list(self._commands.keys())
        expr = re.sub('([^:]+|)',
                      lambda m: re.escape(m.group(1)) + '[^:]*',
                      name)
        commands = sorted(
            list(
                filter(
                    lambda x: re.findall('^%s' % expr, x),
                    all_commands
                )
            )
        )

        if not commands or len(list(filter(lambda x: re.findall('^%s$' % expr, x), commands))) < 1:
            pos = name.find(':')
            if pos >= 0:
                # Check if a namespace exists and contains commands
                self.find_namespace(name[:pos])

            message = 'Command "%s" is not defined.' % name

            alternatives = self.find_alternatives(name, all_commands)
            if alternatives:
                if len(alternatives) == 1:
                    message += '\n\nDid you mean this?\n    '
                else:
                    message += '\n\nDid you mean one of these?\n    '

                message += '\n    '.join(alternatives)

            raise Exception(message)

        # Filter out aliases for commands which are already on the list
        if len(commands) > 1:
            command_list = self._commands

            def f(name_or_alias):
                command_name = command_list[name_or_alias].get_name()

                return command_name == name_or_alias or (command_name not in commands)

            commands = sorted(
                list(
                    filter(
                        f,
                        commands
                    )
                )
            )

        exact = name in commands
        if len(commands) > 1 and not exact:
            suggestions = self.get_abbreviation_suggestions(commands)

            raise Exception('Command "%s" is ambiguous (%s).'
                            % (name, suggestions))

        return self.get(name if exact else commands[0])

    def all(self, namespace=None):
        if namespace is None:
            return self._commands

        commands = {}
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

    def as_text(self, namespace=None, raw=False):
        commands = self.all(self.find_namespace(namespace)) if namespace else self._commands

        width = 0
        for command in commands.values():
            width = len(command.get_name()) if len(command.get_name()) > width else width
        width += 2

        if raw:
            messages = []
            for space, commands in self.sort_commands(commands):
                for name, command in commands:
                    messages.append('%-*s %s' % (width, name, command.get_description()))

                return '\n'.join(messages)

        messages = [self.get_help(), '']
        if namespace:
            messages.append('<comment>Available commands for the \"%s\" namespace:</comment>' % namespace)
        else:
            messages.append('<comment>Available commands:</comment>')

        # add command by namespace
        for space, commands in self.sort_commands(commands):
            if not namespace and '_global' != space:
                messages.append('<comment>' + space + '</comment>')

            for name, command in commands:
                messages.append('  <info>' + '%-*s</info> %s' % (width, name, command.get_description()))

        return '%s\n' % '\n'.join(messages)

    def render_exception(self, e, output_):
        tb = traceback.extract_tb(sys.exc_info()[2])

        title = '  [%s]  ' % e.__class__.__name__
        l = len(title)
        width = self.get_terminal_width(output_)
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

        messages = ['', '']
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
        messages.append('')

        output_.writeln(messages, Output.OUTPUT_RAW)

        if Output.VERBOSITY_VERBOSE <= output_.get_verbosity():
            output_.writeln('<comment>Exception trace:</comment>')

            for exc_info in tb:
                file_ = exc_info[0]
                line_number = exc_info[1]
                function = exc_info[2]
                line = exc_info[3]

                output_.writeln(' <info>%s</info> in <question>%s()</question> '
                                'at line <info>%s</info>'
                                % (file_, function, line_number))
                output_.writeln('   %s' % line)

            output_.writeln('')
            output_.writeln('')

        if self._running_command is not None:
            output_.writeln('<info>%s</info>'
                            % self._running_command.get_synopsis())

            output_.writeln('')
            output_.writeln('')

    def get_terminal_width(self, output_):
        """
        Tries to figure out the terminal width in which this application runs

        @return: The terminal width
        @rtype: int or None
        """
        dimensions = self.get_terminal_dimensions(output_)

        return dimensions[0]

    def get_terminal_height(self, output_):
        """
        Tries to figure out the terminal height in which this application runs

        @return: The terminal height
        @rtype: int or None
        """
        dimensions = self.get_terminal_dimensions(output_)

        return dimensions[1]

    def get_terminal_dimensions(self, output_):
        """
        Tries to figure out the terminal dimensions based on the current environment

        @return: The terminal dimensions
        @rtype: tuple
        """
        if self._terminal_dimensions:
            return self._terminal_dimensions

        try:
            if not isinstance(output_, StreamOutput):
                is_atty = False
            else:
                stream = output_.get_stream()
                is_atty = hasattr(stream, 'fileno') and os.isatty(stream.fileno())
        except UnsupportedOperation:
            is_atty = False

        if not is_atty:
            return None, None

        s = struct.pack("HHHH", 0, 0, 0, 0)
        fd_stdout = output_.get_stream().fileno()
        size = fcntl.ioctl(fd_stdout, termios.TIOCGWINSZ, s)
        height, width = struct.unpack("HHHH", size)[:2]

        return width, height

    def set_terminal_dimensions(self, width, height):
        """
        Sets terminal dimensions.

        Can be useful to force terminal dimensions for functional tests.

        @param width: The width
        @type width: int
        @param height: The height
        @type height: int

        @return: The current application
        @rtype: Application
        """
        self._terminal_dimensions = width, height

        return self

    def configure_io(self, input_, output_):
        """
        Configures the input and output instances based on the user arguments and options.

        @param input_: An Input instance
        @type input_: Input
        @param output_: An Output instance
        @type output_: Output
        """
        if input_.has_parameter_option('--ansi'):
            output_.set_decorated(True)
        elif input_.has_parameter_option('--no-ansi'):
            output_.set_decorated(False)

        if input_.has_parameter_option(['--no-interaction', '-n']):
            input_.set_interactive(False)
        elif self.get_helper_set().has('dialog'):
            input_stream = self.get_helper_set().get('dialog').get_input_stream()
            try:
                is_atty = hasattr(input_stream, 'fileno') and os.isatty(input_stream)
            except UnsupportedOperation:
                is_atty = False

            if not is_atty:
                input_.set_interactive(False)

        if input_.has_parameter_option(['--quiet', '-q']):
            output_.set_verbosity(Output.VERBOSITY_QUIET)
        elif input_.has_parameter_option(['--verbose', '-v']):
            output_.set_verbosity(Output.VERBOSITY_VERBOSE)

    def get_command_name(self, input_):
        return input_.get_first_argument()

    def get_default_input_definition(self):
        return InputDefinition([
            InputArgument('command', InputArgument.REQUIRED, 'The command to execute'),

            InputOption('--help', '-h', InputOption.VALUE_NONE, 'Display this help message.'),
            InputOption('--quiet', '-q', InputOption.VALUE_NONE, 'Do not output any message.'),
            InputOption('--verbose', '-v', InputOption.VALUE_NONE, 'Increase the verbosity of messages.'),
            InputOption('--version', '-V', InputOption.VALUE_NONE, 'Display this application version.'),
            InputOption('--ansi', '', InputOption.VALUE_NONE, 'Force ANSI output.'),
            InputOption('--no-ansi', '', InputOption.VALUE_NONE, 'Disable ANSI output.'),
            InputOption('--no-interaction', '-n', InputOption.VALUE_NONE, 'Do not ask any interactive question.')
        ])

    def get_default_commands(self):
        return [HelpCommand(), ListCommand()]

    def get_default_helper_set(self):
        return HelperSet({
            'formatter': FormatterHelper(),
            'dialog': DialogHelper(),
            'progress': ProgressHelper()
        })

    def sort_commands(self, commands):
        """
        Sorts command in alphabetical order

        @param commands: A dict of commands
        @type commands: dict

        @return: A sorted list of commands
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

    def get_abbreviation_suggestions(self, abbrevs):
        return '%s, %s%s' % \
               (abbrevs[0],
                abbrevs[1],
                ' and %d more' % (len(abbrevs) - 2) if len(abbrevs) > 2 else '')

    def extract_namespace(self, name, limit=None):
        parts = name.split(':')
        parts.pop()

        return ':'.join(parts[:limit] if limit else parts)

    def find_alternatives(self, name, collection):
        """
        Finds alternatives of name in collection

        @param name: The string
        @type name: str
        @param collection: The collection
        @type collection: list

        @return: A sorted list of similar strings
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
                        alternatives[collection_name] = alternatives[collection_name] + lev
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

        alternatives = list(filter(lambda a: a[1] < 2 * threshold, alternatives.items()))
        sorted(alternatives, key=lambda x: x[1])

        return list(map(lambda x: x[0], alternatives))

    def set_default_command(self, command_name):
        """
        Sets the default Command name.

        @param command_name: The Command name
        @type command_name: str
        """
        self._default_command = command_name
