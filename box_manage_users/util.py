# coding: utf-8

from __future__ import unicode_literals
from functools import wraps
import inspect
from itertools import izip
import logging
import sys


def setup_logging(stream_or_file=None, debug=False, name=None):
    logger = logging.getLogger(name)
    if isinstance(stream_or_file, basestring):
        handler = logging.FileHandler(stream_or_file, mode='w')
    else:
        handler = logging.StreamHandler(stream_or_file or sys.stdout)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    return logger


def log_on_success(message, log_level=logging.INFO):
    def wrapper(func):
        argspec = inspect.getargspec(func)

        @wraps(func)
        def wrapped(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            for name, value in izip(argspec.args[1:], args):
                kwargs[name] = value
            logging.log(log_level, message.format(**kwargs))
            return result
        return wrapped
    return wrapper
