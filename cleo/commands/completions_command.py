# -*- coding: utf-8 -*-

import os
import hashlib
import re
import json
import subprocess

from pastel import Pastel

from ..exceptions import InvalidArgument
from ..helpers import DescriptorHelper
from ..outputs import BufferedOutput
from .._compat import encode

from .command import Command
from .completions.templates import TEMPLATES


class CompletionsCommand(Command):
    """
    Generate completion scripts for your shell.
    
    completions
        { shell? : The shell to generate scripts for. }
        { --alias=* : Alias for the current command. } 
    """

    SUPPORTED_SHELLS = ('bash', 'zsh', 'fish')

    hidden = True

    help = """
One can generate a completion script for `<options=bold>%script.name%</>` that is compatible with
a given shell. The script is output on `<options=bold>stdout</>` allowing one to re-direct
the output to the file of their choosing. Where you place the file will
depend on which shell, and which operating system you are using. Your
particular configuration may also determine where these scripts need
to be placed.

Here are some common set ups for the three supported shells under
Unix and similar operating systems (such as GNU/Linux).

<options=bold>BASH</>:

Completion files are commonly stored in `<options=bold>/etc/bash_completion.d/</>`

Run the command:

`<options=bold>%script.name% %command.name% bash > /etc/bash_completion.d/%script.name%.bash-completion</>`

This installs the completion script. You may have to log out and log
back in to your shell session for the changes to take effect.

<options=bold>FISH</>:

Fish completion files are commonly stored in
`<options=bold>$HOME/.config/fish/completions</>`

Run the command:
`<options=bold>%script.name% %command.name% fish > ~/.config/fish/completions/%script.name%.fish</>`

This installs the completion script. You may have to log out and log
back in to your shell session for the changes to take effect.

<options=bold>ZSH</>:

ZSH completions are commonly stored in any directory listed in your
`<options=bold>$fpath</>` variable. To use these completions, you must either add the
generated script to one of those directories, or add your own
to this list.

Adding a custom directory is often the safest best if you're unsure
of which directory to use. First create the directory, for this
example we'll create a hidden directory inside our `<options=bold>$HOME</>` directory

`<options=bold>mkdir ~/.zfunc</>`

Then add the following lines to your `<options=bold>.zshrc</>` just before `<options=bold>compinit</>`

`<options=bold>fpath+=~/.zfunc</>`

Now you can install the completions script using the following command

`<options=bold>%script.name% %command.name% zsh > ~/.zfunc/_%script.name%</>`

You must then either log out and log back in, or simply run

`<options=bold>exec zsh</>`

For the new completions to take affect.

<options=bold>CUSTOM LOCATIONS</>:

Alternatively, you could save these files to the place of your choosing,
such as a custom directory inside your $HOME. Doing so will require you
to add the proper directives, such as `source`ing inside your login
script. Consult your shells documentation for how to add such directives.
"""

    def handle(self):
        shell = self.argument('shell')
        if not shell:
            shell = self.get_shell_type()

        if shell not in self.SUPPORTED_SHELLS:
            raise InvalidArgument(
                '[shell] argument must be one of {}'
                .format(', '.join(self.SUPPORTED_SHELLS))
            )

        self.line(self.render(shell))

    def render(self, shell):
        return getattr(self, 'render_{}'.format(shell))()

    def render_bash(self):
        template = TEMPLATES['bash']

        script_path = self._get_script_full_name()
        script_name = self._get_script_name()
        aliases = [
            script_name,
            script_path
        ]
        aliases += self.option('alias')

        function = self._generate_function_name(script_name, script_path)

        description = self._get_json_description()
        global_options = set([
            '--' + o.get_name()
            for o in self.get_application().get_definition().get_options()
        ])
        commands = []
        options_descriptions = {}
        commands_options = {}
        for command in description['commands']:
            command_options = []
            commands.append(command['name'])

            options = command['definition']['options']
            for name in sorted(list(options.keys())):
                option = options[name]
                name = option['name']
                description = option['description']
                command_options.append(name)
                options_descriptions[name] = description

            commands_options[command['name']] = command_options

        compdefs = '\n'.join([
            'complete -o default -F {} {}'.format(function, alias)
            for alias in aliases
        ])

        commands = sorted(commands)

        command_list = []
        for i, command in enumerate(commands):
            options = set(commands_options[command]).difference(global_options)
            options = sorted(options)
            options = [
                self._zsh_describe(opt, None).strip('"')
                for opt in options
            ]

            desc = [
                '            ({})'.format(command),
                '            opts="${{opts}} {}"'.format(' '.join(options)),
                '            ;;',
            ]

            if i < len(commands) - 1:
                desc.append('')

            command_list.append('\n'.join(desc))

        output = template % {
            'script_name': script_name,
            'function': function,
            'opts': ' '.join(sorted(global_options)),
            'coms': ' '.join(commands),
            'command_list': '\n'.join(command_list),
            'compdefs': compdefs
        }

        return output

    def render_zsh(self):
        template = TEMPLATES['zsh']

        script_path = self._get_script_full_name()
        script_name = self._get_script_name()
        aliases = [script_path]
        aliases += self.option('alias')

        function = self._generate_function_name(script_name, script_path)

        description = self._get_json_description()
        global_options = set([
            '--' + o.get_name()
            for o in self.get_application().get_definition().get_options()
        ])
        commands_descriptions = []
        options_descriptions = {}
        commands_options_descriptions = {}
        commands_options = {}
        for command in description['commands']:
            command_options = []
            commands_options_descriptions[command['name']] = {}
            command_description = self._remove_decoration(command['description'])
            commands_descriptions.append(
                self._zsh_describe(command['name'], command_description)
            )

            options = command['definition']['options']
            for name in sorted(list(options.keys())):
                option = options[name]
                name = option['name']
                description = self._remove_decoration(option['description'])
                command_options.append(name)
                options_descriptions[name] = description
                commands_options_descriptions[command['name']][name] = description

            commands_options[command['name']] = command_options

        compdefs = '\n'.join([
            'compdef {} {}'.format(function, alias)
            for alias in aliases
        ])

        commands = sorted(list(commands_options.keys()))
        command_list = []
        for i, command in enumerate(commands):
            options = set(commands_options[command]).difference(global_options)
            options = sorted(options)
            options = [
                self._zsh_describe(opt, commands_options_descriptions[command][opt])
                for opt in options
            ]

            desc = [
                '            ({})'.format(command),
                '            opts+=({})'.format(' '.join(options)),
                '            ;;',
            ]

            if i < len(commands) - 1:
                desc.append('')

            command_list.append('\n'.join(desc))

        opts = []
        for opt in global_options:
            opts.append(
                self._zsh_describe(opt, options_descriptions[opt])
            )

        output = template % {
            'script_name': script_name,
            'function': function,
            'opts': ' '.join(sorted(opts)),
            'coms': ' '.join(sorted(commands_descriptions)),
            'command_list': '\n'.join(command_list),
            'compdefs': compdefs
        }

        return output

    def render_fish(self):
        template = TEMPLATES['fish']

        script_path = self._get_script_full_name()
        script_name = self._get_script_name()
        aliases = [script_name]
        aliases += self.option('alias')

        function = self._generate_function_name(script_name, script_path)

        description = self._get_json_description()
        global_options = set([
            '--' + o.get_name()
            for o in self.get_application().get_definition().get_options()
        ])
        commands_descriptions = {}
        options_descriptions = {}
        commands_options_descriptions = {}
        commands_options = {}
        for command in description['commands']:
            command_options = []
            commands_options_descriptions[command['name']] = {}
            commands_descriptions[command['name']] = self._remove_decoration(command['description'])

            options = command['definition']['options']
            for name in sorted(list(options.keys())):
                option = options[name]
                name = option['name']
                description = self._remove_decoration(option['description'])
                command_options.append(name)
                options_descriptions[name] = description
                commands_options_descriptions[command['name']][name] = description

            commands_options[command['name']] = command_options

        opts = []
        for opt in sorted(global_options):
            opts.append(
                "complete -c {} -n '__fish{}_no_subcommand' "
                "-l {} -d '{}'"
                .format(
                    script_name,
                    function,
                    opt[2:],
                    options_descriptions[opt].replace("'", "\\'")
                )
            )

        cmds_names = sorted(list(commands_options.keys()))

        cmds = []
        cmds_opts = []
        for i, cmd in enumerate(cmds_names):
            cmds.append(
                "complete -c {} -f -n '__fish{}_no_subcommand' "
                "-a {} -d '{}'"
                .format(
                    script_name,
                    function,
                    cmd,
                    commands_descriptions[cmd].replace("'", "\\'")
                )
            )

            cmds_opts += ['# {}'.format(cmd)]
            options = set(commands_options[cmd]).difference(global_options)
            options = sorted(options)

            for opt in options:
                cmds_opts.append(
                    "complete -c {} -A -n '__fish_seen_subcommand_from {}' "
                    "-l {} -d '{}'"
                    .format(
                        script_name,
                        cmd,
                        opt[2:],
                        commands_options_descriptions[cmd][opt].replace("'", "\\'")
                    )
                )

            if i < len(cmds_names) - 1:
                cmds_opts.append('')

        output = template % {
            'script_name': script_name,
            'function': function,
            'cmds_names': ' '.join(cmds_names),
            'opts': '\n'.join(opts),
            'cmds': '\n'.join(cmds),
            'cmds_opts': '\n'.join(cmds_opts)
        }

        return output

    def get_shell_type(self):
        shell = os.getenv('SHELL')
        if not shell:
            raise RuntimeError(
                'Could not read SHELL environment variable. '
                'Please specify your shell type by passing it as the first argument.'
            )

        return os.path.basename(shell)

    def _get_json_description(self):
        helper = DescriptorHelper()
        output = BufferedOutput()
        helper.describe(
            output,
            self.get_application(),
            format='json'
        )

        return json.loads(output.fetch())

    def _generate_function_name(self, script_name, script_path):
        return '_{}_{}_complete'.format(
            self._sanitize_for_function_name(script_name),
            hashlib.md5(encode(script_path)).hexdigest()[0:16]
        )

    def _sanitize_for_function_name(self, name):
        name = name.replace('-', '_')

        return re.sub('[^A-Za-z0-9_]+', '', name)

    def _zsh_describe(self, value, description=None):
        value = '"' + value.replace(':', '\\:')
        if description:
            description = re.sub(r'(["\'#&;`|*?~<>^()\[\]{}$\\\x0A\xFF])', r'\\\1', description)
            value += ':{}'.format(subprocess.list2cmdline([description]).strip('"'))

        value += '"'

        return value

    def _remove_decoration(self, text):
        return re.sub(
            '\033\\[[^m]*m', '',
            self.output.get_formatter().format(text)
        )
