# -*- coding: utf-8 -*-

from cleo.command import Command


class Foo4Command(Command):

    def configure(self):
        self.set_name('foo3:bar:toh')
