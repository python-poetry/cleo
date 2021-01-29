from cleo.events.event import Event


def test_is_propagation_stopped():
    e = Event()

    assert not e.is_propagation_stopped()


def test_stop_propagation_and_is_propagation_stopped():
    e = Event()

    e.stop_propagation()
    assert e.is_propagation_stopped()
