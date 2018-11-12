# -*- coding: utf-8 -*-

from cleo.commands.command import Command


class SomeCommand(Command):
    def configure(self):
        self.set_name("namespace:name").set_aliases(["name"]).set_description(
            "description"
        ).set_help("help")

    def execute(self, input_, output_):
        output_.writeln("execute called")

    def interact(self, input_, output_):
        output_.writeln("interact called")
