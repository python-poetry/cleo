from __future__ import annotations

from cleo.events.event import Event


def test_is_propagation_not_stopped() -> None:
    e = Event()

    assert not e.is_propagation_stopped()


def test_stop_propagation_and_is_propagation_stopped() -> None:
    e = Event()

    e.stop_propagation()
    assert e.is_propagation_stopped()
