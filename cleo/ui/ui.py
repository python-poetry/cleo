from typing import Dict
from typing import List

from cleo.exceptions import ValueError

from .component import Component


class UI:
    def __init__(self, components: List[Component] = None) -> None:
        self._components: Dict[str, Component] = {}

        if components is None:
            components = []

        for component in components:
            self.register(component)

    def register(self, component: Component) -> None:
        if not isinstance(component, Component):
            raise ValueError("A UI component must inherit from the Component class.")

        if not component.name:
            raise ValueError("A UI component cannot be anonymous.")

        self._components[component.name] = component

    def component(self, name: str) -> Component:
        if name not in self._components:
            raise ValueError(f'UI component "{name}" does not exist.')

        return self._components[name]
