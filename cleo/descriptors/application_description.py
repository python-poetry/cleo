from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from cleo.exceptions import CommandNotFoundException


if TYPE_CHECKING:
    from cleo.application import Application
    from cleo.commands.command import Command


class ApplicationDescription:

    GLOBAL_NAMESPACE = "_global"

    def __init__(
        self,
        application: Application,
        namespace: str | None = None,
        show_hidden: bool = False,
    ) -> None:
        self._application: Application = application
        self._namespace = namespace
        self._show_hidden = show_hidden
        self._namespaces: dict[str, dict[str, str | list[Command]]] = {}
        self._commands: dict[str, Command] = {}
        self._aliases: dict[str, Command] = {}

        self._inspect_application()

    @property
    def namespaces(self) -> dict[str, dict[str, str | list[Command]]]:
        return self._namespaces

    @property
    def commands(self) -> dict[str, Command]:
        return self._commands

    def command(self, name: str) -> Command:
        if name in self._commands:
            return self._commands[name]
        if name in self._aliases:
            return self._aliases[name]
        raise CommandNotFoundException(name)

    def _inspect_application(self) -> None:
        namespace = None
        if self._namespace:
            namespace = self._application.find_namespace(self._namespace)

        all_commands = self._application.all(namespace)

        for namespace, commands in self._sort_commands(all_commands):
            names = []

            for name, command in commands:
                if not command.name or command.hidden:
                    continue

                if command.name == name:
                    self._commands[name] = command
                else:
                    self._aliases[name] = command

                names.append(name)

            self._namespaces[namespace] = {"id": namespace, "commands": names}

    def _sort_commands(
        self, commands: dict[str, Command]
    ) -> list[tuple[str, list[tuple[str, Any]]]]:
        """
        Sorts command in alphabetical order
        """
        namespaced_commands: dict[str, dict[str, Command]] = {}
        for name, command in commands.items():
            key = self._application.extract_namespace(name, 1)
            if not key:
                key = "_global"

            if key in namespaced_commands:
                namespaced_commands[key][name] = command
            else:
                namespaced_commands[key] = {name: command}

        for namespace, commands in namespaced_commands.items():
            namespaced_commands[namespace] = sorted(
                commands.items(), key=lambda x: x[0]
            )

        return sorted(namespaced_commands.items(), key=lambda x: x[0])
