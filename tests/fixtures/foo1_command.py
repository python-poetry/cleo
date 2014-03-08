# -*- coding: utf-8 -*-

from cleo.commands import Command


class Foo1Command(Command):

    def configure(self):
        self.set_name('foo:bar1') \
            .set_description('The foo:bar1 command') \
            .set_aliases(['afoobar1'])

    def execute(self, input_, output_):
        self.input = input_
        self.output = output_
