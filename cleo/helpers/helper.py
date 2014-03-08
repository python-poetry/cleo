# -*- coding: utf-8 -*-


class Helper(object):

    __helper_set = None

    def set_helper_set(self, helper_set=None):
        self.__helper_set = helper_set

    def get_helper_set(self):
        return self.__helper_set