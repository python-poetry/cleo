# -*- coding: utf-8 -*-

from cleo.commands import Command


class FoobarCommand(Command):

    def configure(self):
        self.set_name('foobar:foo') \
            .set_description('The foobar:foo command')

    def execute(self, input_, output_):
        self.input = input_
        self.output = output_
