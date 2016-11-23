# -*- coding: utf-8 -*-

from cleo import Application
from .descriptor_command_1 import DescriptorCommand1
from .descriptor_command_2 import DescriptorCommand2
from .descriptor_command_3 import DescriptorCommand3


class DescriptorApplication2(Application):

    def __init__(self):
        super(DescriptorApplication2, self).__init__('My Cleo application', 'v1.0')

        self.add(DescriptorCommand1())
        self.add(DescriptorCommand2())
        self.add(DescriptorCommand3())
