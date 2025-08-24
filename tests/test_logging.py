from __future__ import annotations

import logging

import pytest

from cleo.application import Application
from cleo.logging.cleo_handler import CleoHandler
from cleo.testers.application_tester import ApplicationTester
from tests.fixtures.foo4_command import Foo4Command


@pytest.fixture
def app() -> Application:
    app = Application()
    cmd = Foo4Command()
    app.add(cmd)
    app._default_command = cmd.name
    return app


@pytest.fixture
def tester(app: Application) -> ApplicationTester:
    app.catch_exceptions(False)
    return ApplicationTester(app)


@pytest.fixture
def root_logger() -> logging.Logger:
    root = logging.getLogger()
    root.setLevel(logging.NOTSET)
    return root


def test_cleohandler_normal(
    tester: ApplicationTester,
    root_logger: logging.Logger,
) -> None:
    handler = CleoHandler(tester.io.output)
    root_logger.addHandler(handler)

    status_code = tester.execute("")

    expected = "This is an warning log record\n" "This is an error log record\n"

    assert status_code == 0
    assert tester.io.fetch_output() == expected


def test_cleohandler_quiet(
    tester: ApplicationTester,
    root_logger: logging.Logger,
) -> None:
    handler = CleoHandler(tester.io.output)
    root_logger.addHandler(handler)

    status_code = tester.execute("-q")

    assert status_code == 0
    assert tester.io.fetch_output() == ""


def test_cleohandler_verbose(
    tester: ApplicationTester,
    root_logger: logging.Logger,
) -> None:
    handler = CleoHandler(tester.io.output)
    root_logger.addHandler(handler)

    status_code = tester.execute("-v")

    expected = (
        "This is an info log record\n"
        "This is an warning log record\n"
        "This is an error log record\n"
    )

    assert status_code == 0
    assert tester.io.fetch_output() == expected


def test_cleohandler_very_verbose(
    tester: ApplicationTester,
    root_logger: logging.Logger,
) -> None:
    handler = CleoHandler(tester.io.output)
    root_logger.addHandler(handler)

    status_code = tester.execute("-vv")

    expected = (
        "This is an debug log record\n"
        "This is an info log record\n"
        "This is an warning log record\n"
        "This is an error log record\n"
    )

    assert status_code == 0
    assert tester.io.fetch_output() == expected


def test_cleohandler_exception_normal(
    tester: ApplicationTester,
    root_logger: logging.Logger,
) -> None:
    handler = CleoHandler(tester.io.output)
    root_logger.addHandler(handler)

    status_code = tester.execute("--exception")

    assert status_code == 0
    lines = tester.io.fetch_output().splitlines()

    assert len(lines) == 7
    assert lines[0] == "This is an exception that I raised"


def test_cleohandler_exception_verbose(
    tester: ApplicationTester,
    root_logger: logging.Logger,
) -> None:
    handler = CleoHandler(tester.io.output)
    root_logger.addHandler(handler)

    status_code = tester.execute("-v --exception")

    assert status_code == 0
    lines = tester.io.fetch_output().splitlines()

    assert len(lines) == 20
    assert lines[0] == "This is an exception that I raised"


def test_cleohandler_exception_very_verbose(
    tester: ApplicationTester,
    root_logger: logging.Logger,
) -> None:
    handler = CleoHandler(tester.io.output)
    root_logger.addHandler(handler)

    status_code = tester.execute("-vv --exception")

    assert status_code == 0
    lines = tester.io.fetch_output().splitlines()

    assert len(lines) == 20
    assert lines[0] == "This is an exception that I raised"
