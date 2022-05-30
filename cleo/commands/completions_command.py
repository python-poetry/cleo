from __future__ import annotations

import hashlib
import inspect
import os
import posixpath
import re
import subprocess

from cleo import helpers
from cleo.commands.command import Command
from cleo.commands.completions.templates import TEMPLATES


class CompletionsCommand(Command):

    name = "completions"
    description = "Generate completion scripts for your shell."

    arguments = [
        helpers.argument(
            "shell", "The shell to generate the scripts for.", optional=True
        )
    ]
    options = [
        helpers.option(
            "alias", None, "Alias for the current command.", flag=False, multiple=True
        )
    ]

    SUPPORTED_SHELLS = ("bash", "zsh", "fish")

    hidden = True

    help = """
One can generate a completion script for `<options=bold>{script_name}</>` that is compatible with \
a given shell. The script is output on `<options=bold>stdout</>` allowing one to re-direct \
the output to the file of their choosing. Where you place the file will \
depend on which shell, and which operating system you are using. Your \
particular configuration may also determine where these scripts need \
to be placed.

Here are some common set ups for the three supported shells under \
Unix and similar operating systems (such as GNU/Linux).

<options=bold>BASH</>:

Completion files are commonly stored in `<options=bold>/etc/bash_completion.d/</>`

Run the command:

`<options=bold>{script_name} {command_name} bash > /etc/bash_completion.d/{script_name}.bash-completion</>`

This installs the completion script. You may have to log out and log \
back in to your shell session for the changes to take effect.

<options=bold>FISH</>:

Fish completion files are commonly stored in\
`<options=bold>$HOME/.config/fish/completions</>`

Run the command:

`<options=bold>{script_name} {command_name} fish > ~/.config/fish/completions/{script_name}.fish</>`

This installs the completion script. You may have to log out and log \
back in to your shell session for the changes to take effect.

<options=bold>ZSH</>:

ZSH completions are commonly stored in any directory listed in your \
`<options=bold>$fpath</>` variable. To use these completions, you must either add the \
generated script to one of those directories, or add your own \
to this list.

Adding a custom directory is often the safest best if you're unsure \
of which directory to use. First create the directory, for this \
example we'll create a hidden directory inside our `<options=bold>$HOME</>` directory

`<options=bold>mkdir ~/.zfunc</>`

Then add the following lines to your `<options=bold>.zshrc</>` just before `<options=bold>compinit</>`

`<options=bold>fpath+=~/.zfunc</>`

Now you can install the completions script using the following command

`<options=bold>{script_name} {command_name} zsh > ~/.zfunc/_{script_name}</>`

You must then either log out and log back in, or simply run

`<options=bold>exec zsh</>`

For the new completions to take affect.

<options=bold>CUSTOM LOCATIONS</>:

Alternatively, you could save these files to the place of your choosing, \
such as a custom directory inside your $HOME. Doing so will require you \
to add the proper directives, such as `source`ing inside your login \
script. Consult your shells documentation for how to add such directives.
"""

    def handle(self) -> int:
        shell = self.argument("shell")
        if not shell:
            shell = self.get_shell_type()

        if shell not in self.SUPPORTED_SHELLS:
            raise ValueError(
                "[shell] argument must be one of {}".format(
                    ", ".join(self.SUPPORTED_SHELLS)
                )
            )

        self.line(self.render(shell))

        return 0

    def render(self, shell: str) -> str:
        return getattr(self, f"render_{shell}")()

    def render_bash(self) -> str:
        template = TEMPLATES["bash"]

        script_name = self._io.input.script_name
        if not script_name:
            script_name = inspect.stack()[-1][1]

        script_path = posixpath.realpath(script_name)
        script_name = os.path.basename(script_path)
        aliases = [script_name, script_path]
        aliases += self.option("alias")

        function = self._generate_function_name(script_name, script_path)

        commands = []
        global_options = set()
        options_descriptions = {}
        commands_options = {}
        for option in self.application.definition.options:
            options_descriptions[
                "--" + option.name
            ] = self.io.output.formatter.remove_format(option.description)
            global_options.add("--" + option.name)

        for command in self.application.all().values():
            if not command.enabled or command.hidden:
                continue

            command_options = []
            commands.append(command.name)

            options = command.definition.options
            for option in sorted(options, key=lambda o: o.name):
                name = "--" + option.name
                description = option.description
                command_options.append(name)
                options_descriptions[name] = description

            commands_options[command.name] = command_options

        compdefs = "\n".join(
            [f"complete -o default -F {function} {alias}" for alias in aliases]
        )

        commands = sorted(commands)

        command_list = []
        for i, command in enumerate(commands):
            options = set(commands_options[command]).difference(global_options)
            options = sorted(options)
            options = [self._zsh_describe(opt, None).strip('"') for opt in options]

            desc = [
                f"            ({command})",
                '            opts="${{opts}} {}"'.format(" ".join(options)),
                "            ;;",
            ]

            if i < len(commands) - 1:
                desc.append("")

            command_list.append("\n".join(desc))

        output = template % {
            "script_name": script_name,
            "function": function,
            "opts": " ".join(sorted(global_options)),
            "coms": " ".join(commands),
            "command_list": "\n".join(command_list),
            "compdefs": compdefs,
        }

        return output

    def render_zsh(self):
        template = TEMPLATES["zsh"]

        script_name = self._io.input.script_name
        if not script_name:
            script_name = inspect.stack()[-1][1]

        script_path = posixpath.realpath(script_name)
        script_name = os.path.basename(script_path)
        aliases = [script_path]
        aliases += self.option("alias")

        function = self._generate_function_name(script_name, script_path)

        global_options = set()
        commands_descriptions = []
        options_descriptions = {}
        commands_options_descriptions = {}
        commands_options = {}
        for option in self.application.definition.options:
            options_descriptions[
                "--" + option.name
            ] = self.io.output.formatter.remove_format(option.description)
            global_options.add("--" + option.name)

        for command in self.application.all().values():
            if not command.enabled or command.hidden:
                continue

            command_options = []
            commands_options_descriptions[command.name] = {}
            command_description = self._io.output.formatter.remove_format(
                command.description
            )
            commands_descriptions.append(
                self._zsh_describe(command.name, command_description)
            )

            options = command.definition.options
            for option in sorted(options, key=lambda o: o.name):
                name = "--" + option.name
                description = self.io.output.formatter.remove_format(option.description)
                command_options.append(name)
                options_descriptions[name] = description
                commands_options_descriptions[command.name][name] = description

            commands_options[command.name] = command_options

        compdefs = "\n".join([f"compdef {function} {alias}" for alias in aliases])

        commands = sorted(commands_options.keys())
        command_list = []
        for i, command in enumerate(commands):
            options = set(commands_options[command]).difference(global_options)
            options = sorted(options)
            options = [
                self._zsh_describe(opt, commands_options_descriptions[command][opt])
                for opt in options
            ]

            desc = [
                f"            ({command})",
                "            opts+=({})".format(" ".join(options)),
                "            ;;",
            ]

            if i < len(commands) - 1:
                desc.append("")

            command_list.append("\n".join(desc))

        opts = []
        for opt in global_options:
            opts.append(self._zsh_describe(opt, options_descriptions[opt]))

        output = template % {
            "script_name": script_name,
            "function": function,
            "opts": " ".join(sorted(opts)),
            "coms": " ".join(sorted(commands_descriptions)),
            "command_list": "\n".join(command_list),
            "compdefs": compdefs,
        }

        return output

    def render_fish(self):
        template = TEMPLATES["fish"]

        script_name = self._io.input.script_name
        if not script_name:
            script_name = inspect.stack()[-1][1]

        script_path = posixpath.realpath(script_name)
        script_name = os.path.basename(script_path)
        aliases = [script_name]
        aliases += self.option("alias")

        function = self._generate_function_name(script_name, script_path)

        global_options = set()
        commands_descriptions = {}
        options_descriptions = {}
        commands_options_descriptions = {}
        commands_options = {}
        for option in self.application.definition.options:
            options_descriptions[
                "--" + option.name
            ] = self._io.output.formatter.remove_format(option.description)
            global_options.add("--" + option.name)

        for command in self.application.all().values():
            if not command.enabled or command.hidden:
                continue

            command_options = []
            commands_options_descriptions[command.name] = {}
            commands_descriptions[
                command.name
            ] = self._io.output.formatter.remove_format(command.description)

            options = command.definition.options
            for option in sorted(options, key=lambda o: o.name):
                name = "--" + option.name
                description = self._io.output.formatter.remove_format(
                    option.description
                )
                command_options.append(name)
                options_descriptions[name] = description
                commands_options_descriptions[command.name][name] = description

            commands_options[command.name] = command_options

        opts = []
        for opt in sorted(global_options):
            opts.append(
                "complete -c {} -n '__fish{}_no_subcommand' "
                "-l {} -d '{}'".format(
                    script_name,
                    function,
                    opt[2:],
                    options_descriptions[opt].replace("'", "\\'"),
                )
            )

        cmds_names = sorted(commands_options.keys())

        cmds = []
        cmds_opts = []
        for i, cmd in enumerate(cmds_names):
            cmds.append(
                "complete -c {} -f -n '__fish{}_no_subcommand' "
                "-a {} -d '{}'".format(
                    script_name,
                    function,
                    cmd,
                    commands_descriptions[cmd].replace("'", "\\'"),
                )
            )

            cmds_opts += [f"# {cmd}"]
            options = set(commands_options[cmd]).difference(global_options)
            options = sorted(options)

            for opt in options:
                cmds_opts.append(
                    "complete -c {} -A -n '__fish_seen_subcommand_from {}' "
                    "-l {} -d '{}'".format(
                        script_name,
                        cmd,
                        opt[2:],
                        commands_options_descriptions[cmd][opt].replace("'", "\\'"),
                    )
                )

            if i < len(cmds_names) - 1:
                cmds_opts.append("")

        output = template % {
            "script_name": script_name,
            "function": function,
            "cmds_names": " ".join(cmds_names),
            "opts": "\n".join(opts),
            "cmds": "\n".join(cmds),
            "cmds_opts": "\n".join(cmds_opts),
        }

        return output

    def get_shell_type(self) -> str:
        shell = os.getenv("SHELL")
        if not shell:
            raise RuntimeError(
                "Could not read SHELL environment variable. "
                "Please specify your shell type by passing it as the first argument."
            )

        return os.path.basename(shell)

    def _generate_function_name(self, script_name: str, script_path: str) -> str:
        return "_{}_{}_complete".format(
            self._sanitize_for_function_name(script_name),
            hashlib.md5(script_path.encode()).hexdigest()[0:16],
        )

    def _sanitize_for_function_name(self, name: str) -> str:
        name = name.replace("-", "_")

        return re.sub("[^A-Za-z0-9_]+", "", name)

    def _zsh_describe(self, value: str, description: str | None = None) -> str:
        value = '"' + value.replace(":", "\\:")
        if description:
            description = re.sub(
                r'(["\'#&;`|*?~<>^()\[\]{}$\\\x0A\xFF])', r"\\\1", description
            )
            value += ":{}".format(subprocess.list2cmdline([description]).strip('"'))

        value += '"'

        return value
