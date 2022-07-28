from __future__ import annotations

from io import StringIO

import pytest

from cleo.io.outputs.section_output import SectionOutput


@pytest.fixture()
def stream() -> StringIO:
    return StringIO()


@pytest.fixture()
def sections() -> list[SectionOutput]:
    return []


@pytest.fixture()
def output(stream: StringIO, sections: list[SectionOutput]) -> SectionOutput:
    return SectionOutput(stream, sections, decorated=True)


@pytest.fixture()
def output2(stream: StringIO, sections: list[SectionOutput]) -> SectionOutput:
    return SectionOutput(stream, sections, decorated=True)


def test_clear_all(output: SectionOutput, stream: StringIO) -> None:
    output.write_line("Foo\nBar")
    output.clear()

    stream.seek(0)

    assert stream.read() == "Foo\nBar\n\x1b[2A\x1b[0J"


def test_clear_with_number_of_lines(output: SectionOutput, stream: StringIO) -> None:
    output.write_line("Foo\nBar\nBaz\nFooBar")
    output.clear(2)

    stream.seek(0)

    assert stream.read() == "Foo\nBar\nBaz\nFooBar\n\x1b[2A\x1b[0J"


def test_clear_with_number_of_lines_and_multiple_sections(
    output: SectionOutput, output2: SectionOutput, stream: StringIO
) -> None:
    output2.write_line("Foo")
    output2.write_line("Bar")
    output2.clear(1)
    output.write_line("Baz")

    stream.seek(0)

    assert stream.read() == "Foo\nBar\n\x1b[1A\x1b[0J\x1b[1A\x1b[0JBaz\nFoo\n"


def test_clear_preserves_empty_lines(
    output: SectionOutput, output2: SectionOutput, stream: StringIO
) -> None:
    output2.write_line("\nFoo")
    output2.clear(1)
    output.write_line("Bar")

    stream.seek(0)

    assert stream.read() == "\nFoo\n\x1b[1A\x1b[0J\x1b[1A\x1b[0JBar\n\n"


def test_overwrite(output: SectionOutput, stream: StringIO) -> None:
    output.write_line("Foo")
    output.overwrite("Bar")

    stream.seek(0)

    assert stream.read() == "Foo\n\x1b[1A\x1b[0JBar\n"


def test_overwrite_multiple_lines(output: SectionOutput, stream: StringIO) -> None:
    output.write_line("Foo\nBar\nBaz")
    output.overwrite("Bar")

    stream.seek(0)

    assert stream.read() == "Foo\nBar\nBaz\n\x1b[3A\x1b[0JBar\n"


def test_add_multiple_sections(
    output: SectionOutput, output2: SectionOutput, sections: list[SectionOutput]
) -> None:
    assert len(sections) == 2


def test_multiple_sections_output(
    output: SectionOutput, output2: SectionOutput, stream: StringIO
) -> None:
    output.write_line("Foo")
    output2.write_line("Bar")

    output.overwrite("Baz")
    output2.overwrite("Foobar")

    stream.seek(0)

    assert (
        stream.read()
        == "Foo\nBar\n\x1b[2A\x1b[0JBar\n\x1b[1A\x1b[0JBaz\nBar\n\x1b[1A\x1b[0JFoobar\n"
    )
