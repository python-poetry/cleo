# -*- coding: utf-8 -*-
import re

import pytest

from cleo.io.buffered_io import BufferedIO
from cleo.io.outputs.output import Verbosity
from cleo.ui.exception_trace import ExceptionTrace


def fail():
    raise Exception("Failed")


def test_render_better_error_message():
    io = BufferedIO()

    try:
        raise Exception("Failed")
    except Exception as e:
        trace = ExceptionTrace(e)

    trace.render(io)

    expected = """\

  Exception

  Failed

  at {}:19 in test_render_better_error_message
       15│ def test_render_better_error_message():
       16│     io = BufferedIO()
       17│ 
       18│     try:
    →  19│         raise Exception("Failed")
       20│     except Exception as e:
       21│         trace = ExceptionTrace(e)
       22│ 
       23│     trace.render(io)
""".format(
        trace._get_relative_file_path(__file__)
    )
    assert expected == io.fetch_output()


def test_render_debug_better_error_message():
    io = BufferedIO()
    io.set_verbosity(Verbosity.DEBUG)

    try:
        fail()
    except Exception as e:  # Exception
        trace = ExceptionTrace(e)

    trace.render(io)

    expected = r"""^
  Stack trace:

  1  {}:52 in test_render_debug_better_error_message
       50\│ 
       51\│     try:
    →  52\│         fail\(\)
       53\│     except Exception as e:  # Exception
       54\│         trace = ExceptionTrace\(e\)

  Exception

  Failed

  at {}:12 in fail
        8\│ from cleo.ui.exception_trace import ExceptionTrace
        9\│ 
       10\│ 
       11\│ def fail\(\):
    →  12\│     raise Exception\("Failed"\)
       13\│ 
       14\│ 
       15\│ def test_render_better_error_message\(\):
       16\│     io = BufferedIO\(\)
""".format(
        re.escape(trace._get_relative_file_path(__file__)),
        re.escape(trace._get_relative_file_path(__file__)),
    )

    assert re.match(expected, io.fetch_output()) is not None


def recursion_error():
    recursion_error()


def test_render_debug_better_error_message_recursion_error():
    io = BufferedIO()
    io.set_verbosity(Verbosity.DEBUG)

    try:
        recursion_error()
    except RecursionError as e:
        trace = ExceptionTrace(e)

    trace.render(io)

    expected = r"""^
  Stack trace:

  \d+  {}:99 in test_render_debug_better_error_message_recursion_error
         97\│ 
         98\│     try:
      →  99\│         recursion_error\(\)
        100\│     except RecursionError as e:
        101\│         trace = ExceptionTrace\(e\)

  ...  Previous frame repeated \d+ times

  \s*\d+  {}:91 in recursion_error
         89\│ 
         90\│ def recursion_error\(\):
      →  91\│     recursion_error\(\)
         92\│ 
         93\│ 

  RecursionError

  maximum recursion depth exceeded

  at {}:91 in recursion_error
       87\│     assert re.match\(expected, io.fetch_output\(\)\) is not None
       88\│ 
       89\│ 
       90\│ def recursion_error\(\):
    →  91\│     recursion_error\(\)
       92\│ 
       93\│ 
       94\│ def test_render_debug_better_error_message_recursion_error\(\):
       95\│     io = BufferedIO\(\)
""".format(
        re.escape(trace._get_relative_file_path(__file__)),
        re.escape(trace._get_relative_file_path(__file__)),
        re.escape(trace._get_relative_file_path(__file__)),
    )

    assert re.match(expected, io.fetch_output()) is not None


def test_render_verbose_better_error_message():
    io = BufferedIO()
    io.set_verbosity(Verbosity.VERBOSE)

    try:
        fail()
    except Exception as e:  # Exception
        trace = ExceptionTrace(e)

    trace.render(io)

    expected = r"""^
  Stack trace:

  1  {}:152 in test_render_verbose_better_error_message
       fail\(\)

  Exception

  Failed

  at {}:12 in fail
        8\│ from cleo.ui.exception_trace import ExceptionTrace
        9\│ 
       10\│ 
       11\│ def fail\(\):
    →  12\│     raise Exception\("Failed"\)
       13\│ 
       14\│ 
       15\│ def test_render_better_error_message\(\):
       16\│     io = BufferedIO\(\)
""".format(
        re.escape(trace._get_relative_file_path(__file__)),
        re.escape(trace._get_relative_file_path(__file__)),
    )

    assert re.match(expected, io.fetch_output()) is not None


def first():
    def second():
        first()

    second()


def test_render_debug_better_error_message_recursion_error_with_multiple_duplicated_frames():
    io = BufferedIO()
    io.set_verbosity(Verbosity.VERBOSE)

    with pytest.raises(RecursionError) as e:
        first()

    trace = ExceptionTrace(e.value)

    trace.render(io)

    expected = r"...  Previous 2 frames repeated \d+ times"

    assert re.search(expected, io.fetch_output()) is not None


def test_render_can_ignore_given_files():
    import os

    from .helpers import outer

    io = BufferedIO()
    io.set_verbosity(Verbosity.VERBOSE)

    def call():
        def run():
            outer()

        run()

    with pytest.raises(Exception) as e:
        call()

    trace = ExceptionTrace(e.value)
    helpers_file = os.path.join(os.path.dirname(__file__), "helpers.py")
    trace.ignore_files_in("^{}$".format(re.escape(helpers_file)))

    trace.render(io)

    expected = """
  Stack trace:

  2  {}:224 in test_render_can_ignore_given_files
       call()

  1  {}:221 in call
       run()

  Exception

  Foo

  at {}:3 in inner
        1│ def outer():
        2│     def inner():
    →   3│         raise Exception("Foo")
        4│ 
        5│     inner()
        6│ 
""".format(
        trace._get_relative_file_path(__file__),
        trace._get_relative_file_path(__file__),
        trace._get_relative_file_path(helpers_file),
    )

    assert expected == io.fetch_output()


def test_render_shows_ignored_files_if_in_debug_mode():
    import os

    from .helpers import outer

    io = BufferedIO()
    io.set_verbosity(Verbosity.DEBUG)

    def call():
        def run():
            outer()

        run()

    with pytest.raises(Exception) as e:
        call()

    trace = ExceptionTrace(e.value)
    helpers_file = os.path.join(os.path.dirname(__file__), "helpers.py")
    trace.ignore_files_in("^{}$".format(re.escape(helpers_file)))

    trace.render(io)

    expected = """
  Stack trace:

  4  {}:276 in test_render_shows_ignored_files_if_in_debug_mode
      274│ 
      275│     with pytest.raises(Exception) as e:
    → 276│         call()
      277│ 
      278│     trace = ExceptionTrace(e.value)

  3  {}:273 in call
      271│             outer()
      272│ 
    → 273│         run()
      274│ 
      275│     with pytest.raises(Exception) as e:

  2  {}:271 in run
      269│     def call():
      270│         def run():
    → 271│             outer()
      272│ 
      273│         run()

  1  {}:5 in outer
        3│         raise Exception("Foo")
        4│ 
    →   5│     inner()
        6│ 

  Exception

  Foo

  at {}:3 in inner
        1│ def outer():
        2│     def inner():
    →   3│         raise Exception("Foo")
        4│ 
        5│     inner()
        6│ 
""".format(
        trace._get_relative_file_path(__file__),
        trace._get_relative_file_path(__file__),
        trace._get_relative_file_path(__file__),
        trace._get_relative_file_path(helpers_file),
        trace._get_relative_file_path(helpers_file),
    )

    assert expected == io.fetch_output()


def test_render_supports_solutions():
    from crashtest.contracts.base_solution import BaseSolution
    from crashtest.contracts.provides_solution import ProvidesSolution
    from crashtest.solution_providers.solution_provider_repository import (
        SolutionProviderRepository,
    )

    class CustomError(ProvidesSolution, Exception):
        @property
        def solution(self):
            solution = BaseSolution("Solution Title.", "Solution Description")
            solution.documentation_links.append("https://example.com")
            solution.documentation_links.append("https://example2.com")

            return solution

    io = BufferedIO()

    def call():
        raise CustomError("Error with solution")

    with pytest.raises(CustomError) as e:
        call()

    trace = ExceptionTrace(
        e.value, solution_provider_repository=SolutionProviderRepository()
    )

    trace.render(io)

    expected = """
  CustomError

  Error with solution

  at {}:355 in call
      351│ 
      352│     io = BufferedIO()
      353│ 
      354│     def call():
    → 355│         raise CustomError("Error with solution")
      356│ 
      357│     with pytest.raises(CustomError) as e:
      358│         call()
      359│ 

  • Solution Title: Solution Description
    https://example.com,
    https://example2.com
""".format(
        trace._get_relative_file_path(__file__),
    )

    assert expected == io.fetch_output()


def test_render_falls_back_on_ascii_symbols():
    from crashtest.contracts.base_solution import BaseSolution
    from crashtest.contracts.provides_solution import ProvidesSolution
    from crashtest.solution_providers.solution_provider_repository import (
        SolutionProviderRepository,
    )

    class CustomError(ProvidesSolution, Exception):
        @property
        def solution(self):
            solution = BaseSolution("Solution Title.", "Solution Description")
            solution.documentation_links.append("https://example.com")
            solution.documentation_links.append("https://example2.com")

            return solution

    io = BufferedIO(supports_utf8=False)

    def call():
        raise CustomError("Error with solution")

    with pytest.raises(CustomError) as e:
        call()

    trace = ExceptionTrace(
        e.value, solution_provider_repository=SolutionProviderRepository()
    )

    trace.render(io)

    expected = """
  CustomError

  Error with solution

  at {}:411 in call
      407| 
      408|     io = BufferedIO(supports_utf8=False)
      409| 
      410|     def call():
    > 411|         raise CustomError("Error with solution")
      412| 
      413|     with pytest.raises(CustomError) as e:
      414|         call()
      415| 

  * Solution Title: Solution Description
    https://example.com,
    https://example2.com
""".format(
        trace._get_relative_file_path(__file__),
    )

    assert expected == io.fetch_output()
