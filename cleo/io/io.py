from typing import Iterable
from typing import Optional
from typing import Union

from .inputs.input import Input
from .outputs.output import Output
from .outputs.output import Type as OutputType
from .outputs.output import Verbosity
from .outputs.section_output import SectionOutput


class IO:
    def __init__(self, input: Input, output: Output, error_output: Output) -> None:
        self._input = input
        self._output = output
        self._error_output = error_output

    @property
    def input(self) -> Input:
        return self._input

    @property
    def output(self) -> Output:
        return self._output

    @property
    def error_output(self) -> Output:
        return self._error_output

    def read(self, length: int, default: Optional[str] = None) -> str:
        """
        Reads the given amount of characters from the input stream.
        """
        return self._input.read(length, default=default)

    def read_line(
        self, length: Optional[int] = None, default: Optional[str] = None
    ) -> str:
        """
        Reads a line from the input stream.
        """
        return self._input.read_line(length=length, default=default)

    def write_line(
        self,
        messages: Union[str, Iterable[str]],
        verbosity: Verbosity = Verbosity.NORMAL,
        type: OutputType = OutputType.NORMAL,
    ) -> None:
        self._output.write_line(messages, verbosity=verbosity, type=type)

    def write(
        self,
        messages: Union[str, Iterable[str]],
        new_line: bool = False,
        verbosity: Verbosity = Verbosity.NORMAL,
        type: OutputType = OutputType.NORMAL,
    ) -> None:
        self._output.write(messages, new_line=new_line, verbosity=verbosity, type=type)

    def write_error_line(
        self,
        messages: Union[str, Iterable[str]],
        verbosity: Verbosity = Verbosity.NORMAL,
        type: OutputType = OutputType.NORMAL,
    ) -> None:
        self._error_output.write_line(messages, verbosity=verbosity, type=type)

    def write_error(
        self,
        messages: Union[str, Iterable[str]],
        new_line: bool = False,
        verbosity: Verbosity = Verbosity.NORMAL,
        type: OutputType = OutputType.NORMAL,
    ) -> None:
        self._error_output.write(
            messages, new_line=new_line, verbosity=verbosity, type=type
        )

    def overwrite(self, messages: Union[str, Iterable[str]]) -> None:
        from cleo.cursor import Cursor

        cursor = Cursor(self._output)
        cursor.move_to_column(1)
        cursor.clear_line()
        self.write(messages)

    def overwrite_error(self, messages: Union[str, Iterable[str]]) -> None:
        from cleo.cursor import Cursor

        cursor = Cursor(self._error_output)
        cursor.move_to_column(1)
        cursor.clear_line()
        self.write_error(messages)

    def flush(self) -> None:
        self._output.flush()

    def is_interactive(self) -> bool:
        return self._input.is_interactive()

    def interactive(self, interactive: bool = True) -> None:
        self._input.interactive(interactive)

    def decorated(self, decorated: bool = True) -> None:
        self._output.decorated(decorated)
        self._error_output.decorated(decorated)

    def is_decorated(self) -> bool:
        return self._output.is_decorated()

    def supports_utf8(self) -> bool:
        return self._output.supports_utf8()

    def set_verbosity(self, verbosity: Verbosity) -> None:
        self._output.set_verbosity(verbosity)
        self._error_output.set_verbosity(verbosity)

    def is_verbose(self) -> bool:
        return self.output.is_verbose()

    def is_very_verbose(self) -> bool:
        return self.output.is_very_verbose()

    def is_debug(self) -> bool:
        return self.output.is_debug()

    def set_input(self, input: Input) -> None:
        self._input = input

    def with_input(self, input: Input) -> "IO":
        return self.__class__(input, self._output, self._error_output)

    def remove_format(self, text: str) -> str:
        return self._output.remove_format(text)

    def section(self) -> SectionOutput:
        return self._output.section()
