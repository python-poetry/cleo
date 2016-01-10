# -*- coding: utf-8 -*-

from .helper import Helper
from ..descriptors import TextDescriptor, JsonDescriptor, MarkdownDescriptor


class DescriptorHelper(Helper):
    """
    This class adds helper method to describe objects in various formats.
    """

    def __init__(self):
        self._descriptors = {}

        self.register('txt', TextDescriptor())
        self.register('json', JsonDescriptor())
        self.register('md', MarkdownDescriptor())

    def describe(self, output, obj, **options):
        """
        Describes an object if supported.

        Available options are:
            * format: string, the output format name
            * raw_text: boolean, sets output type as raw

        :type output: Output
        :type obj: mixed
        """
        actual_options = {
            'raw_text': False,
            'format': 'txt'
        }

        actual_options.update(options)

        if actual_options['format'] not in self._descriptors:
            raise ValueError('Unsupported format "%s".' % actual_options['format'])

        descriptor = self._descriptors[options['format']]
        descriptor.describe(output, obj, **options)

    def register(self, name, descriptor):
        """
        Registers a descriptor.

        :param name: The name of the descriptor
        :type name: str

        :param descriptor: The descriptor to register
        :type descriptor: Descriptor

        :rtype: DescriptorHelper
        """
        self._descriptors[name] = descriptor

        return self
