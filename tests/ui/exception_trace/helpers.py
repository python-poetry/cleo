from __future__ import annotations


def simple_exception() -> None:
    raise ValueError("Simple Exception")


def nested_exception() -> None:
    try:
        simple_exception()
    except ValueError:
        raise RuntimeError("Nested Exception")  # noqa: B904


def recursive_exception() -> None:
    def inner() -> None:
        outer()

    def outer() -> None:
        inner()

    inner()
