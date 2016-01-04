# -*- coding: utf-8 -*-

from ..inputs import (
    InputArgument, InputOption, InputDefinition
)

from ..commands import BaseCommand
from ..exceptions import CleoException
from ..outputs import Output


class Descriptor(object):

    output = None

    def describe(self, output, obj, **options):
        """
        Describes an InputArgument instance.

        :param output: An OutputInstance
        :type output: Output

        :param obj: The object to describe
        :type obj: mixed

        :param options: The options
        :type options: dict
        """
        from ..application import Application

        self.output = output

        if isinstance(obj, InputArgument):
            self._describe_input_argument(obj, **options)
        elif isinstance(obj, InputOption):
            self._describe_input_option(obj, **options)
        elif isinstance(obj, InputDefinition):
            self._describe_input_definition(obj, **options)
        elif isinstance(obj, BaseCommand):
            self._describe_command(obj, **options)
        elif isinstance(obj, Application):
            self._describe_application(obj, **options)
        else:
            raise CleoException('Object of type "%s" is not describable' % obj.__class__.__name__)

    def _write(self, content, decorated=False):
        """
        Writes content to output.

        :param content: The content to write
        :type content: str

        type decorated: bool
        """
        output_type = Output.OUTPUT_RAW
        if decorated:
            output_type = Output.OUTPUT_NORMAL

        self.output.write(content, False, output_type)

    def _describe_input_argument(self, argument, **options):
        """
        Describes an InputArgument instance.

        :type argument: InputArgument
        :type options: dict
        """
        raise NotImplementedError()

    def _describe_input_option(self, option, **options):
        """
        Describes an InputOption instance.

        :type argument: InputOption
        :type options: dict
        """
        raise NotImplementedError()

    def _describe_input_definition(self, definition, **options):
        """
        Describes an InputDefinition instance.

        :type argument: InputDefinition
        :type options: dict
        """
        raise NotImplementedError()

    def _describe_command(self, command, **options):
        """
        Describes a Command instance.

        :type argument: BaseCommand
        :type options: dict
        """
        raise NotImplementedError()

    def _describe_application(self, application, **options):
        """
        Describes an Application instance.

        :type argument: Application
        :type options: dict
        """
        raise NotImplementedError()
