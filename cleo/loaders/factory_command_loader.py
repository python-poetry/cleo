from typing import Callable
from typing import Dict
from typing import List

from cleo.commands.command import Command

from ..exceptions import CommandNotFoundException
from .command_loader import CommandLoader


class FactoryCommandLoader(CommandLoader):
    """
    A simple command loader using factories to instantiate commands lazily.
    """

    def __init__(self, factories: Dict[str, Callable]) -> None:
        self._factories = factories

    @property
    def names(self) -> List[str]:
        return list(self._factories.keys())

    def has(self, name: str) -> bool:
        return name in self._factories

    def get(self, name: str) -> Command:
        if name not in self._factories:
            raise CommandNotFoundException(name)

        factory = self._factories[name]

        return factory()
