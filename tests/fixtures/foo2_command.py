# -*- coding: utf-8 -*-

from cleo.commands import Command


class Foo2Command(Command):
    def configure(self):
        self.set_name("foo1:bar").set_description("The foo1:bar command").set_aliases(
            ["afoobar2"]
        )

    def execute(self, input_, output_):
        pass
