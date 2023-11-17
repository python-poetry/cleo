# NOTE: these tests reference line numbers from code in this file,
# so it's sensitive to refactoring
from __future__ import annotations

import re

import pytest

from cleo.io.buffered_io import BufferedIO
from cleo.io.outputs.output import Verbosity
from cleo.ui.exception_trace.component import ExceptionTrace
from tests.fixtures.exceptions import nested1
from tests.fixtures.exceptions import nested2
from tests.fixtures.exceptions import recursion
from tests.fixtures.exceptions import simple


def test_render_better_error_message() -> None:
    io = BufferedIO()

    try:
        simple.simple_exception()
    except Exception as e:
        trace = ExceptionTrace(e)

    trace.render(io)

    expected = f"""\

  Exception

  Failed

  at {trace._get_relative_file_path(simple.__file__)}:2 in simple_exception
        1│ def simple_exception() -> None:
    →   2│     raise Exception("Failed")
        3│ 
"""
    assert expected == io.fetch_output()


def test_render_debug_better_error_message() -> None:
    io = BufferedIO()
    io.set_verbosity(Verbosity.DEBUG)

    try:
        simple.simple_exception()
    except Exception as e:  # Exception
        trace = ExceptionTrace(e)

    trace.render(io)

    lineno = 47
    expected = f"""
  Stack trace:

  1  {trace._get_relative_file_path(__file__)}:{lineno} in \
test_render_debug_better_error_message
       {lineno - 2}│ 
       {lineno - 1}│     try:
    →  {lineno + 0}│         simple.simple_exception()
       {lineno + 1}│     except Exception as e:  # Exception
       {lineno + 2}│         trace = ExceptionTrace(e)

  Exception

  Failed

  at {trace._get_relative_file_path(simple.__file__)}:2 in simple_exception
        1│ def simple_exception() -> None:
    →   2│     raise Exception("Failed")
        3│ 
"""

    assert io.fetch_output() == expected


def test_render_debug_better_error_message_recursion_error() -> None:
    io = BufferedIO()
    io.set_verbosity(Verbosity.DEBUG)

    try:
        recursion.recursion_error()
    except RecursionError as e:
        trace = ExceptionTrace(e)

    lineno = 83
    trace.render(io)

    expected = rf"""^
  Stack trace:

  \d+  {re.escape(trace._get_relative_file_path(__file__))}:{lineno} in test_render_debug_better_error_message_recursion_error
         {lineno - 2}\│ 
         {lineno - 1}\│     try:
      →  {lineno + 0}\│         recursion.recursion_error\(\)
         {lineno + 1}\│     except RecursionError as e:
         {lineno + 2}\│         trace = ExceptionTrace\(e\)

  ...  Previous frame repeated \d+ times

  \s*\d+  {re.escape(trace._get_relative_file_path(recursion.__file__))}:2 in recursion_error
          1\│ def recursion_error\(\) -> None:
      →   2\│     recursion_error\(\)
          3\│ 

  RecursionError

  maximum recursion depth exceeded

  at {re.escape(trace._get_relative_file_path(recursion.__file__))}:2 in recursion_error
        1\│ def recursion_error\(\) -> None:
    →   2\│     recursion_error\(\)
        3\│ 
"""

    assert re.match(expected, io.fetch_output()) is not None


def test_render_very_verbose_better_error_message() -> None:
    io = BufferedIO()
    io.set_verbosity(Verbosity.VERY_VERBOSE)

    try:
        simple.simple_exception()
    except Exception as e:  # Exception
        trace = ExceptionTrace(e)

    trace.render(io)

    expected = f"""
  Stack trace:

  1  {trace._get_relative_file_path(__file__)}:125 in \
test_render_very_verbose_better_error_message
       simple.simple_exception()

  Exception

  Failed

  at {trace._get_relative_file_path(simple.__file__)}:2 in simple_exception
        1│ def simple_exception() -> None:
    →   2│     raise Exception("Failed")
        3│ 
"""

    assert expected == io.fetch_output()


def test_render_debug_better_error_message_recursion_error_with_multiple_duplicated_frames() -> (
    None
):
    def first() -> None:
        def second() -> None:
            first()

        second()

    io = BufferedIO()
    io.set_verbosity(Verbosity.VERY_VERBOSE)

    with pytest.raises(RecursionError) as e:
        first()

    trace = ExceptionTrace(e.value)

    trace.render(io)

    expected = r"...  Previous 2 frames repeated \d+ times"

    assert re.search(expected, io.fetch_output()) is not None


def test_render_can_ignore_given_files() -> None:
    io = BufferedIO()
    io.set_verbosity(Verbosity.VERY_VERBOSE)

    with pytest.raises(Exception) as e:
        nested2.call()

    trace = ExceptionTrace(e.value)
    trace.ignore_files_in(rf"^{re.escape(nested1.__file__)}$")
    trace.render(io)

    lineno = 180
    expected = f"""
  Stack trace:

  2  {trace._get_relative_file_path(__file__)}:{lineno} in \
test_render_can_ignore_given_files
       nested2.call()

  1  {trace._get_relative_file_path(nested2.__file__)}:8 in call
       run()

  Exception

  Foo

  at {trace._get_relative_file_path(nested1.__file__)}:3 in inner
        1│ def outer() -> None:
        2│     def inner() -> None:
    →   3│         raise Exception("Foo")
        4│ 
        5│     inner()
        6│ 
"""

    assert io.fetch_output() == expected


def test_render_shows_ignored_files_if_in_debug_mode() -> None:
    io = BufferedIO()
    io.set_verbosity(Verbosity.DEBUG)

    with pytest.raises(Exception) as e:
        nested2.call()

    trace = ExceptionTrace(e.value)
    trace.ignore_files_in(rf"^{re.escape(nested1.__file__)}$")

    trace.render(io)
    lineno = 218
    expected = f"""
  Stack trace:

  4  {trace._get_relative_file_path(__file__)}:{lineno} in \
test_render_shows_ignored_files_if_in_debug_mode
      {lineno - 2}│ 
      {lineno - 1}│     with pytest.raises(Exception) as e:
    → {lineno + 0}│         nested2.call()
      {lineno + 1}│ 
      {lineno + 2}│     trace = ExceptionTrace(e.value)

  3  {trace._get_relative_file_path(nested2.__file__)}:8 in call
        6│         outer()
        7│ 
    →   8│     run()
        9│ 

  2  {trace._get_relative_file_path(nested2.__file__)}:6 in run
        4│ def call() -> None:
        5│     def run() -> None:
    →   6│         outer()
        7│ 
        8│     run()

  1  {trace._get_relative_file_path(nested1.__file__)}:5 in outer
        3│         raise Exception("Foo")
        4│ 
    →   5│     inner()
        6│ 

  Exception

  Foo

  at {trace._get_relative_file_path(nested1.__file__)}:3 in inner
        1│ def outer() -> None:
        2│     def inner() -> None:
    →   3│         raise Exception("Foo")
        4│ 
        5│     inner()
        6│ 
"""

    assert io.fetch_output() == expected


def test_render_falls_back_on_ascii_symbols() -> None:
    io = BufferedIO(supports_utf8=False)

    with pytest.raises(Exception) as e:
        simple.simple_exception()

    trace = ExceptionTrace(e.value)

    trace.render(io)

    expected = f"""
  Exception

  Failed

  at {trace._get_relative_file_path(simple.__file__)}:2 in simple_exception
        1| def simple_exception() -> None:
    >   2|     raise Exception("Failed")
        3| 
"""

    assert io.fetch_output() == expected


def test_empty_source_file_do_not_break_highlighter() -> None:
    from cleo.ui.exception_trace.component import Highlighter

    highlighter = Highlighter()
    highlighter.highlighted_lines("")


def test_docstrings_are_correctly_rendered() -> None:
    from cleo.formatters.formatter import Formatter
    from cleo.ui.exception_trace.component import Highlighter

    source = '''
def test():
    """
    Doctring
    """
    ...
'''

    formatter = Formatter()
    highlighter = Highlighter()
    lines = highlighter.highlighted_lines(source)

    assert [formatter.format(line) for line in lines] == [*source.splitlines(), ""]


def test_simple_render() -> None:
    io = BufferedIO()

    with pytest.raises(Exception) as e:
        simple.simple_exception()

    trace = ExceptionTrace(e.value)

    trace.render(io, simple=True)

    expected = """
Failed
"""

    assert io.fetch_output() == expected


def test_simple_render_aborts_if_no_message() -> None:
    io = BufferedIO()

    with pytest.raises(Exception) as e:
        raise AssertionError

    trace = ExceptionTrace(e.value)

    trace.render(io, simple=True)
    lineno = 342

    expected = f"""
  AssertionError

  

  at {trace._get_relative_file_path(__file__)}:{lineno} in \
test_simple_render_aborts_if_no_message
      {lineno - 4}│ def test_simple_render_aborts_if_no_message() -> None:
      {lineno - 3}│     io = BufferedIO()
      {lineno - 2}│ 
      {lineno - 1}│     with pytest.raises(Exception) as e:
    → {lineno + 0}│         raise AssertionError
      {lineno + 1}│ 
      {lineno + 2}│     trace = ExceptionTrace(e.value)
      {lineno + 3}│ 
      {lineno + 4}│     trace.render(io, simple=True)
"""
    assert expected == io.fetch_output()
