import operator
import pytest


class ConfigException(Exception):
    pass


def checkconfig(x):
    __tracebackhide__ = lambda e: isinstance(e, ConfigException)
    if not hasattr(x, "config"):
        raise ConfigException("not configured: {}".format(x))


def test_something():
    checkconfig(42)
