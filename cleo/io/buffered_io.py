from typing import Optional
from typing import cast

from .inputs.input import Input
from .io import IO
from .outputs.buffered_output import BufferedOutput


class BufferedIO(IO):
    def __init__(
        self,
        input: Optional[Input] = None,
        decorated: bool = False,
        supports_utf8: bool = True,
    ) -> None:
        super(BufferedIO, self).__init__(
            input,
            BufferedOutput(decorated=decorated, supports_utf8=supports_utf8),
            BufferedOutput(decorated=decorated, supports_utf8=supports_utf8),
        )

        self._output = cast(BufferedOutput, self._output)
        self._error_output = cast(BufferedOutput, self._error_output)

    def fetch_output(self) -> str:
        return self._output.fetch()

    def fetch_error(self) -> str:
        return self._error_output.fetch()

    def clear(self) -> None:
        self._output.clear()
        self._error_output.clear()

    def clear_output(self) -> None:
        self._output.clear()

    def clear_error(self) -> None:
        self._error_output.clear()

    def supports_utf8(self) -> bool:
        return self._output.supports_utf8()

    def clear_user_input(self) -> None:
        self._input.stream.truncate(0)
        self._input.stream.seek(0)

    def set_user_input(self, user_input: str) -> None:
        self.clear_user_input()

        self._input.stream.write(user_input)
        self._input.stream.seek(0)
