# -*- coding: utf-8 -*-

import os
from io import BytesIO

from ..inputs.list_input import ListInput
from ..outputs.stream_output import StreamOutput


class ApplicationTester(object):
    """
    Eases the testing of console applications.
    """

    def __init__(self, application):
        """
        Constructor

        :param application: A Application instance to test
        :type application: Application
        """
        self._application = application
        self._input = None
        self._output = None
        self._inputs = []

    def run(self, input_, options=None):
        """
        Executes the command

        Available options:
            * interactive: Sets the input interactive flag
            * decorated: Sets the output decorated flag
            * verbosity: Sets the output verbosity flag

        :param input_: A dict of argument and options
        :type input_: list
        :param options: A dict of options
        :type options: dict

        :return: The command exit code
        :rtype: integer
        """
        options = options or {}

        self._input = ListInput(input_)
        if self._inputs:
            self._input.set_stream(self._create_stream(self._inputs))

        if 'interactive' in options:
            self._input.set_interactive(options['interactive'])

        self._output = StreamOutput(BytesIO())
        if 'decorated' in options:
            self._output.set_decorated(options['decorated'])
        else:
            self._output.set_decorated(False)

        if 'verbosity' in options:
            self._output.set_verbosity(options['verbosity'])

        self._application.run(self._input, self._output)

    def get_display(self, normalize=False):
        """
        Gets the display returned by the last execution command

        :return: The display
        :rtype: str
        """
        self._output.get_stream().seek(0)

        display = self._output.get_stream().read().decode('utf-8')

        if normalize:
            display = display.replace(os.linesep, '\n')

        return display

    def get_input(self):
        """
        Gets the input instance used by the last execution of the command.

        :return: The current input instance
        :rtype: Input
        """
        return self._input

    def get_output(self):
        """
        Gets the output instance used by the last execution of the command.

        :return: The current output instance
        :rtype: Output
        """
        return self._output

    def set_inputs(self, inputs):
        """
        Sets the user inputs.

        :param inputs: The user inputs
        :type inputs: list

        :rtype: CommandTester
        """
        self._inputs = inputs

        return self

    def _create_stream(self, inputs):
        """
        Create a stream from inputs.

        :type inputs: list

        :rtype:
        """
        stream = BytesIO()
        stream.write(os.linesep.join(inputs).encode())
        stream.seek(0)

        return stream
