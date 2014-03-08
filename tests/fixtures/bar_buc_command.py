# -*- coding: utf-8 -*-

from cleo.commands import Command


class BarBucCommand(Command):

    def configure(self):
        self.set_name('bar:buc')
