from __future__ import annotations

import os

from io import StringIO

import pytest

from cleo.io.outputs.stream_output import StreamOutput


@pytest.fixture()
def stream() -> StringIO:
    return StringIO()


@pytest.mark.parametrize(
    ["env", "is_decorated"],
    [
        ({"NO_COLOR": "1"}, False),
        ({"FORCE_COLOR": "1"}, True),
    ],
)
def test_is_decorated_respects_environment(
    stream: StringIO, environ: None, env: dict[str, str], is_decorated: bool
) -> None:
    os.environ.update(env)

    output = StreamOutput(stream)
    output.write_line("<fg=blue>FooBar</>")
    stream.seek(0)

    assert output.is_decorated() == is_decorated
    expected = "\x1b[34mFooBar\x1b[39m\n" if is_decorated else "FooBar\n"
    assert stream.read() == expected
