from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from cleo.application import Application
from cleo.testers.application_tester import ApplicationTester
from tests.fixtures.foo4_command import Foo4Command


if TYPE_CHECKING:
    from cleo.commands.command import Command


@pytest.mark.parametrize("cmd", (Foo4Command(),))
def test_run_with_logging_integration_normal(cmd: Command) -> None:
    app = Application()
    app.add(cmd)

    tester = ApplicationTester(app)
    status_code = tester.execute(f"{cmd.name}")

    expected = "This is an warning log record\n" "This is an error log record\n"

    assert status_code == 0
    assert tester.io.fetch_output() == expected


@pytest.mark.parametrize("cmd", (Foo4Command(),))
def test_run_with_logging_integration_quiet(cmd: Command) -> None:
    app = Application()
    app.add(cmd)

    tester = ApplicationTester(app)
    status_code = tester.execute(f"{cmd.name} -q")

    assert status_code == 0
    assert tester.io.fetch_output() == ""


@pytest.mark.parametrize("cmd", (Foo4Command(),))
def test_run_with_logging_integration_verbose(cmd: Command) -> None:
    app = Application()
    app.add(cmd)

    tester = ApplicationTester(app)
    status_code = tester.execute(f"{cmd.name} -v")

    expected = (
        "This is an info log record\n"
        "This is an warning log record\n"
        "This is an error log record\n"
    )

    assert status_code == 0
    assert tester.io.fetch_output() == expected


@pytest.mark.parametrize("cmd", (Foo4Command(),))
def test_run_with_logging_integration_very_verbose(cmd: Command) -> None:
    app = Application()
    app.add(cmd)

    tester = ApplicationTester(app)
    status_code = tester.execute(f"{cmd.name} -vv")

    expected = (
        "This is an debug log record\n"
        "This is an info log record\n"
        "This is an warning log record\n"
        "This is an error log record\n"
    )

    assert status_code == 0
    assert tester.io.fetch_output() == expected
