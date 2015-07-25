# -*- coding: utf-8 -*-

import sys

PY2 = sys.version_info[0] == 2

if PY2:
    long = long
    unicode = unicode
    basestring = basestring
else:
    long = int
    unicode = str
    basestring = str


def decode_str(string, encodings=None):
    if not PY2 and not isinstance(string, bytes):
        return string

    if encodings is None:
        encodings = ['utf-8', 'latin1', 'ascii']

    for encoding in encodings:
        try:
            return string.decode(encoding)
        except UnicodeDecodeError:
            pass

    return string.decode(encodings[0], errors='ignore')
