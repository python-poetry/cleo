def outer() -> None:
    def inner() -> None:
        raise Exception("Foo")

    inner()
