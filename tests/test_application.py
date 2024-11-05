from __future__ import annotations

import os
import sys

from pathlib import Path

import pytest

from cleo.application import Application
from cleo.commands.command import Command
from cleo.exceptions import CleoCommandNotFoundError
from cleo.exceptions import CleoNamespaceNotFoundError
from cleo.io.io import IO
from cleo.io.outputs.stream_output import StreamOutput
from cleo.testers.application_tester import ApplicationTester
from tests.fixtures.foo1_command import Foo1Command
from tests.fixtures.foo2_command import Foo2Command
from tests.fixtures.foo3_command import Foo3Command
from tests.fixtures.foo_command import FooCommand
from tests.fixtures.foo_sub_namespaced1_command import FooSubNamespaced1Command
from tests.fixtures.foo_sub_namespaced2_command import FooSubNamespaced2Command
from tests.fixtures.foo_sub_namespaced3_command import FooSubNamespaced3Command


FIXTURES_PATH = Path(__file__).parent.joinpath("fixtures")


@pytest.fixture()
def app() -> Application:
    return Application()


@pytest.fixture()
def tester(app: Application) -> ApplicationTester:
    app.catch_exceptions(False)

    return ApplicationTester(app)


def test_name_version_getters() -> None:
    app = Application("foo", "bar")

    assert app.name == "foo"
    assert app.display_name == "Foo"
    assert app.version == "bar"


def test_name_version_setter() -> None:
    app = Application("foo", "bar")

    app.set_name("bar")
    app.set_version("foo")

    assert app.name == "bar"
    assert app.display_name == "Bar"
    assert app.version == "foo"

    app.set_display_name("Baz")

    assert app.display_name == "Baz"


def test_long_version() -> None:
    app = Application("foo", "bar")

    assert app.long_version == "<b>Foo</b> (version <c1>bar</c1>)"


def test_help(app: Application) -> None:
    assert app.help == FIXTURES_PATH.joinpath("application_help.txt").read_text()


def test_all(app: Application) -> None:
    commands = app.all()

    assert isinstance(commands["help"], Command)

    app.add(FooCommand())

    assert len(app.all("foo")) == 1


def test_add(app: Application) -> None:
    foo = FooCommand()
    app.add(foo)
    commands = app.all()

    assert [commands["foo bar"]] == [foo]

    foo1 = Foo1Command()
    app.add(foo1)

    commands = app.all()

    assert [commands["foo bar"], commands["foo bar1"]] == [foo, foo1]


def test_has_get(app: Application) -> None:
    assert app.has("list")
    assert not app.has("afoobar")

    foo = FooCommand()
    app.add(foo)

    assert app.has("foo bar")
    assert app.has("afoobar")
    assert app.get("foo bar") == foo
    assert app.get("afoobar") == foo


def test_silent_help(app: Application) -> None:
    app.catch_exceptions(False)

    tester = ApplicationTester(app)
    tester.execute("-h -q", decorated=False)

    assert tester.io.fetch_output() == ""


def test_get_namespaces(app: Application) -> None:
    app.add(FooCommand())
    app.add(Foo1Command())

    assert app.get_namespaces() == ["foo"]


def test_find_namespace(app: Application) -> None:
    app.add(FooCommand())

    assert app.find_namespace("foo") == "foo"


def test_find_namespace_with_sub_namespaces(app: Application) -> None:
    app.add(FooSubNamespaced1Command())
    app.add(FooSubNamespaced2Command())

    assert app.find_namespace("foo") == "foo"


def test_find_ambiguous_namespace(app: Application) -> None:
    app.add(FooCommand())
    app.add(Foo2Command())

    with pytest.raises(
        CleoNamespaceNotFoundError,
        match=(
            r'There are no commands in the "f" namespace\.\n\n'
            r"Did you mean this\?\n    foo"
        ),
    ):
        app.find_namespace("f")


def test_find_invalid_namespace(app: Application) -> None:
    app.add(FooCommand())
    app.add(Foo2Command())

    with pytest.raises(
        CleoNamespaceNotFoundError,
        match=r'There are no commands in the "bar" namespace\.',
    ):
        app.find_namespace("bar")


def test_find_unique_name_but_namespace_name(app: Application) -> None:
    app.add(FooCommand())
    app.add(Foo1Command())
    app.add(Foo2Command())

    with pytest.raises(
        CleoCommandNotFoundError,
        match=r'The command "foo1" does not exist\.',
    ):
        app.find("foo1")


def test_find(app: Application) -> None:
    app.add(FooCommand())

    assert isinstance(app.find("foo bar"), FooCommand)
    assert isinstance(app.find("afoobar"), FooCommand)


def test_find_ambiguous_command(app: Application) -> None:
    app.add(FooCommand())

    with pytest.raises(
        CleoCommandNotFoundError,
        match=(
            r'The command "foo b" does not exist\.\n\nDid you mean this\?\n    foo bar'
        ),
    ):
        app.find("foo b")


def test_find_ambiguous_command_hidden(app: Application) -> None:
    foo = FooCommand()
    foo.hidden = True
    app.add(foo)

    with pytest.raises(
        CleoCommandNotFoundError,
        match=r'The command "foo b" does not exist\.$',
    ):
        app.find("foo b")


def test_set_catch_exceptions(app: Application, environ: dict[str, str]) -> None:
    app.auto_exits(False)
    os.environ["COLUMNS"] = "120"

    tester = ApplicationTester(app)
    app.catch_exceptions(True)

    assert app.are_exceptions_caught()

    tester.execute("foo", decorated=False)

    assert tester.io.fetch_output() == ""
    assert (
        tester.io.fetch_error()
        == FIXTURES_PATH.joinpath("application_exception1.txt").read_text()
    )

    app.catch_exceptions(False)

    with pytest.raises(CleoCommandNotFoundError):
        tester.execute("foo", decorated=False)


def test_auto_exit(app: Application) -> None:
    app.auto_exits(False)
    assert not app.is_auto_exit_enabled()

    app.auto_exits()
    assert app.is_auto_exit_enabled()


def test_run(app: Application, argv: list[str]) -> None:
    app.catch_exceptions(False)
    app.auto_exits(False)
    command = Foo1Command()
    app.add(command)

    sys.argv = ["console", "foo bar1"]
    app.run()

    assert isinstance(command.io, IO)
    assert isinstance(command.io.output, StreamOutput)
    assert isinstance(command.io.error_output, StreamOutput)
    assert command.io.output.stream == sys.stdout
    assert command.io.error_output.stream == sys.stderr


def test_run_runs_the_list_command_without_arguments(tester: ApplicationTester) -> None:
    tester.execute("", decorated=False)

    assert (
        tester.io.fetch_output()
        == FIXTURES_PATH.joinpath("application_run1.txt").read_text()
    )


def test_run_runs_help_command_if_required(tester: ApplicationTester) -> None:
    tester.execute("--help", decorated=False)

    assert (
        tester.io.fetch_output()
        == FIXTURES_PATH.joinpath("application_run2.txt").read_text()
    )

    tester.execute("-h", decorated=False)

    assert (
        tester.io.fetch_output()
        == FIXTURES_PATH.joinpath("application_run2.txt").read_text()
    )


def test_run_runs_help_command_with_command(tester: ApplicationTester) -> None:
    tester.execute("--help list", decorated=False)

    assert (
        tester.io.fetch_output()
        == FIXTURES_PATH.joinpath("application_run3.txt").read_text()
    )

    tester.execute("list -h", decorated=False)

    assert (
        tester.io.fetch_output()
        == FIXTURES_PATH.joinpath("application_run3.txt").read_text()
    )


def test_run_removes_all_output_if_quiet(tester: ApplicationTester) -> None:
    tester.execute("list --quiet")

    assert tester.io.fetch_output() == ""

    tester.execute("list -q")

    assert tester.io.fetch_output() == ""


def test_run_with_verbosity(tester: ApplicationTester) -> None:
    tester.execute("list --verbose")

    assert tester.io.is_verbose()

    tester.execute("list -v")

    assert tester.io.is_verbose()

    tester.execute("list -vv")

    assert tester.io.is_very_verbose()

    tester.execute("list -vvv")

    assert tester.io.is_debug()


def test_run_with_version(tester: ApplicationTester) -> None:
    tester.execute("--version")

    assert (
        tester.io.fetch_output()
        == FIXTURES_PATH.joinpath("application_run4.txt").read_text()
    )

    tester.execute("-V")

    assert (
        tester.io.fetch_output()
        == FIXTURES_PATH.joinpath("application_run4.txt").read_text()
    )


def test_run_with_help(tester: ApplicationTester) -> None:
    tester.execute("help --help")

    assert (
        tester.io.fetch_output()
        == FIXTURES_PATH.joinpath("application_run5.txt").read_text()
    )

    tester.execute("-h help")

    assert (
        tester.io.fetch_output()
        == FIXTURES_PATH.joinpath("application_run5.txt").read_text()
    )


def test_run_with_input() -> None:
    app = Application()
    command = Foo3Command()
    app.add(command)

    tester = ApplicationTester(app)
    status_code = tester.execute("foo3", inputs="Hello world!")

    assert status_code == 0
    assert tester.io.fetch_output() == "Hello world!\n"


def test_run_namespaced_with_input() -> None:
    app = Application()
    command = FooSubNamespaced3Command()
    app.add(command)

    tester = ApplicationTester(app)
    status_code = tester.execute("foo bar", inputs="Hello world!")

    assert status_code == 0
    assert tester.io.fetch_output() == "Hello world!\n"


@pytest.mark.parametrize("cmd", (Foo3Command(), FooSubNamespaced3Command()))
def test_run_with_input_and_non_interactive(cmd: Command) -> None:
    app = Application()
    app.add(cmd)

    tester = ApplicationTester(app)
    status_code = tester.execute(f"--no-interaction {cmd.name}", inputs="Hello world!")

    assert status_code == 0
    assert tester.io.fetch_output() == "default input\n"
