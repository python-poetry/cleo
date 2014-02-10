# -*- coding: utf-8 -*-

from cleo.command import Command


class BarBucCommand(Command):

    def configure(self):
        self.set_name('bar:buc')
