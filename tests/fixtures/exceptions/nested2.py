from tests.fixtures.exceptions.nested1 import outer


def call() -> None:
    def run() -> None:
        outer()

    run()
