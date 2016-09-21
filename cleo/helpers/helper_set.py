# -*- coding: utf-8 -*-


class HelperSet(object):

    def __init__(self, helpers=None):
        helpers = helpers or []

        self.__helpers = {}
        self.__command = None

        for helper in helpers:
            self.set(helper, None)

    def set(self, helper, alias=None):
        self.__helpers[helper.get_name()] = helper
        if alias is not None:
            self.__helpers[alias] = helper

        helper.set_helper_set(self)

    def has(self, name):
        return name in self.__helpers

    def get(self, name):
        if not self.has(name):
            raise Exception('The helper "%s" is not defined.' % name)

        return self.__helpers[name]

    def set_command(self, command):
        self.__command = command

    def get_command(self):
        return self.__command
