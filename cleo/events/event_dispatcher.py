from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Callable


if TYPE_CHECKING:
    from cleo.events.event import Event


class EventDispatcher:
    def __init__(self) -> None:
        self._listeners = {}
        self._sorted = {}

    def dispatch(self, event: Event, event_name: str | None = None) -> Event:
        if event_name is None:
            event_name = event.__class__.__name__

        listeners = self.get_listeners(event_name)

        if listeners:
            self._do_dispatch(listeners, event_name, event)

        return event

    def get_listeners(
        self, event_name: str | None = None
    ) -> list[Callable] | dict[str, Callable]:
        if event_name is not None:
            if event_name not in self._listeners:
                return []

            if event_name not in self._sorted:
                self._sort_listeners(event_name)

            return self._sorted[event_name]

        for event_name in self._listeners.keys():
            if event_name not in self._sorted:
                self._sort_listeners(event_name)

        return self._sorted

    def get_listener_priority(self, event_name: str, listener: Callable) -> int | None:
        if event_name not in self._listeners:
            return

        for priority, listeners in self._listeners[event_name].items():
            for v in listeners:
                if v == listener:
                    return priority

    def has_listeners(self, event_name: str | None = None) -> bool:
        if event_name is not None:
            if event_name not in self._listeners:
                return False

            return len(self._listeners[event_name]) > 0

        return any(self._listeners.values())

    def add_listener(
        self, event_name: str, listener: Callable, priority: int = 0
    ) -> None:
        if event_name not in self._listeners:
            self._listeners[event_name] = {}

        if priority not in self._listeners[event_name]:
            self._listeners[event_name][priority] = []

        self._listeners[event_name][priority].append(listener)

        if event_name in self._sorted:
            del self._sorted[event_name]

    def _do_dispatch(
        self, listeners: list[Callable], event_name: str, event: Event
    ) -> None:
        for listener in listeners:
            if event.is_propagation_stopped():
                break

            listener(event, event_name, self)

    def _sort_listeners(self, event_name: str) -> None:
        """
        Sorts the internal list of listeners for the given event by priority.
        """
        self._sorted[event_name] = []

        for _, listeners in sorted(
            self._listeners[event_name].items(), key=lambda t: -t[0]
        ):
            for listener in listeners:
                self._sorted[event_name].append(listener)
