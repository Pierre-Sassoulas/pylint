"""Regression test for https://github.com/pylint-dev/pylint/issues/9811.

A property with a setter was inferred as the instance itself, so its
members were reported as ``no-member``.
"""

# pylint: disable=missing-function-docstring,missing-class-docstring


class BugReport:
    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value: str):
        self._host = value

    @property
    def timezone(self):
        return self.host.lower()
