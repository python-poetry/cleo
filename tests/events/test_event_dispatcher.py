from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from cleo.events.event import Event
from cleo.events.event_dispatcher import EventDispatcher


if TYPE_CHECKING:
    from typing import Any


@pytest.fixture()
def dispatcher() -> EventDispatcher:
    return EventDispatcher()


@pytest.fixture()
def listener() -> EventListener:
    return EventListener()


PRE_FOO = "pre.foo"
POST_FOO = "post.foo"
PRE_BAR = "pre.bar"
POST_BAR = "post.bar"


class EventListener:
    def __init__(self) -> None:
        self.pre_foo_invoked = False
        self.post_foo_invoked = False

    def pre_foo(self, *_: Any) -> None:
        self.pre_foo_invoked = True

    def post_foo(self, e: Event, *_: Any) -> None:
        self.post_foo_invoked = True
        e.stop_propagation()


def test_initial_state(dispatcher: EventDispatcher) -> None:
    assert {} == dispatcher.get_listeners()
    assert not dispatcher.has_listeners(PRE_FOO)
    assert not dispatcher.has_listeners(POST_FOO)


def test_add_listener(dispatcher: EventDispatcher, listener: EventListener) -> None:
    dispatcher.add_listener(PRE_FOO, listener.pre_foo)
    dispatcher.add_listener(POST_FOO, listener.post_foo)

    assert dispatcher.has_listeners()
    assert dispatcher.has_listeners(PRE_FOO)
    assert dispatcher.has_listeners(POST_FOO)
    assert len(dispatcher.get_listeners(PRE_FOO)) == 1
    assert len(dispatcher.get_listeners(POST_FOO)) == 1
    assert len(dispatcher.get_listeners()) == 2


def test_get_listeners_sorts_by_priority(dispatcher: EventDispatcher) -> None:
    listener1 = EventListener()
    listener2 = EventListener()
    listener3 = EventListener()

    dispatcher.add_listener(PRE_FOO, listener1.pre_foo, -10)
    dispatcher.add_listener(PRE_FOO, listener2.pre_foo, 10)
    dispatcher.add_listener(PRE_FOO, listener3.pre_foo)

    expected = [listener2.pre_foo, listener3.pre_foo, listener1.pre_foo]

    assert expected == dispatcher.get_listeners(PRE_FOO)


def test_get_all_listeners_sorts_by_priority(dispatcher: EventDispatcher) -> None:
    listener1 = EventListener()
    listener2 = EventListener()
    listener3 = EventListener()
    listener4 = EventListener()
    listener5 = EventListener()
    listener6 = EventListener()

    dispatcher.add_listener(PRE_FOO, listener1.pre_foo, -10)
    dispatcher.add_listener(PRE_FOO, listener2.pre_foo)
    dispatcher.add_listener(PRE_FOO, listener3.pre_foo, 10)

    dispatcher.add_listener(POST_FOO, listener4.pre_foo, -10)
    dispatcher.add_listener(POST_FOO, listener5.pre_foo)
    dispatcher.add_listener(POST_FOO, listener6.pre_foo, 10)

    expected = {
        PRE_FOO: [listener3.pre_foo, listener2.pre_foo, listener1.pre_foo],
        POST_FOO: [listener6.pre_foo, listener5.pre_foo, listener4.pre_foo],
    }

    assert dispatcher.get_listeners() == expected


def test_get_listener_priority(dispatcher: EventDispatcher) -> None:
    listener1 = EventListener()
    listener2 = EventListener()

    dispatcher.add_listener(PRE_FOO, listener1.pre_foo, -10)
    dispatcher.add_listener(PRE_FOO, listener2.pre_foo)

    assert dispatcher.get_listener_priority(PRE_FOO, listener1.pre_foo) == -10
    assert dispatcher.get_listener_priority(PRE_FOO, listener2.pre_foo) == 0
    assert dispatcher.get_listener_priority(PRE_BAR, listener2.pre_foo) is None


def test_dispatch(dispatcher: EventDispatcher, listener: EventListener) -> None:
    dispatcher.add_listener(PRE_FOO, listener.pre_foo)
    dispatcher.add_listener(POST_FOO, listener.post_foo)
    dispatcher.dispatch(Event(), PRE_FOO)
    assert listener.pre_foo_invoked
    assert not listener.post_foo_invoked


def test_stop_event_propagation(
    dispatcher: EventDispatcher, listener: EventListener
) -> None:
    other_listener = EventListener()

    dispatcher.add_listener(POST_FOO, listener.post_foo, 10)
    dispatcher.add_listener(POST_FOO, other_listener.post_foo)
    dispatcher.dispatch(Event(), POST_FOO)

    assert listener.post_foo_invoked
    assert not other_listener.post_foo_invoked
