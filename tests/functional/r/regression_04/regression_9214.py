"""Regression test for https://github.com/pylint-dev/pylint/issues/9214.

A property built from ``functools.partial`` failed a ``CallContext``
assertion when inferred.
"""

# pylint: disable=missing-function-docstring,missing-class-docstring,too-few-public-methods

import functools


class MockClass:
    def _get_option(self, option):
        return option

    enabled = property(functools.partial(_get_option, option="Enabled"))

    @property
    def supported_types(self):
        return ["tcp", "udp"] if self.enabled else []
