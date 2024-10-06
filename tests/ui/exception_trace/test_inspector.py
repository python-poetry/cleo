from __future__ import annotations

from cleo.ui.exception_trace.inspector import Inspector
from tests.ui.exception_trace.helpers import nested_exception
from tests.ui.exception_trace.helpers import recursive_exception
from tests.ui.exception_trace.helpers import simple_exception


def test_inspector_with_simple_exception() -> None:
    try:
        simple_exception()
    except ValueError as e:
        inspector = Inspector(e)

        assert inspector.exception == e
        assert not inspector.has_previous_exception()
        assert inspector.previous_exception is None
        assert inspector.exception_name == "ValueError"
        assert inspector.exception_message == "Simple Exception"
        assert len(inspector.frames) > 0


def test_inspector_with_nested_exception() -> None:
    try:
        nested_exception()
    except RuntimeError as e:
        inspector = Inspector(e)

        assert inspector.exception == e
        assert inspector.has_previous_exception()
        assert inspector.previous_exception is not None
        assert inspector.exception_name == "RuntimeError"
        assert inspector.exception_message == "Nested Exception"
        assert len(inspector.frames) > 0
        assert len(inspector.frames.compact()) == 1


def test_inspector_with_recursive_exception() -> None:
    try:
        recursive_exception()
    except RuntimeError as e:
        inspector = Inspector(e)

        assert inspector.exception == e
        assert not inspector.has_previous_exception()
        assert inspector.previous_exception is None
        assert inspector.exception_name == "RecursionError"
        assert inspector.exception_message == "maximum recursion depth exceeded"
        assert len(inspector.frames) > 0
        assert len(inspector.frames) > len(inspector.frames.compact())
