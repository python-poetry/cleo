from typing import List

from cleo.commands.command import Command


class CommandLoader:
    @property
    def names(self) -> List[str]:
        """
        All registered command names.
        """
        raise NotImplementedError()

    def get(self, name: str) -> Command:
        """
        Loads a command.
        """
        raise NotImplementedError()

    def has(self, name: str) -> bool:
        """
        Checks whether a command exists or not.
        """
        raise NotImplementedError()
