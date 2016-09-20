# -*- coding: utf-8 -*-


class CleoException(Exception):

    def __init__(self, message, code=1):
        self.code = code
        
        super(CleoException, self).__init__(message)


class UsageException(CleoException):
    
    def __init__(self, message, code=2):
        super(UsageException, self).__init__(message, code)
