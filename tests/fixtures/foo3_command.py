# -*- coding: utf-8 -*-

from cleo.commands import Command


class Foo3Command(Command):
    def configure(self):
        self.set_name("foo3:bar").set_description("The foo3:bar command")

    def execute(self, input_, output_):
        try:
            try:
                raise Exception("First exception <p>this is html</p>")
            except Exception as e:
                raise Exception("Second exception <comment>comment</comment>")
        except Exception as e:
            raise Exception("Third exception <fg=blue;bg=red>comment</>")
