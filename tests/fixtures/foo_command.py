# -*- coding: utf-8 -*-

from cleo.commands import Command


class FooCommand(Command):

    def configure(self):
        self.set_name('foo:bar') \
            .set_description('The foo:bar command') \
            .set_aliases(['afoobar'])

    def interact(self, input_, output_):
        output_.writeln('interact called')

    def execute(self, input_, output_):
        self.input = input_
        self.output = output_

        output_.writeln('called')


def foo_code(input_, output_):
    output_.writeln('called')


foo_commmand = {
    'foo:bar1': {
        'description': 'The foo:bar command',
        'aliases': ['afoobar'],
        'code': foo_code
    }
}
