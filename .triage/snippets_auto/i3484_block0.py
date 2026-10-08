#!/usr/bin/env python3
"""Module."""

# A PyPI package - run pylint in a venv _without_ this installed!
import cached_property


class Klass:
    """Klass."""

    def __init__(self, arg):
        self.arg = arg

    def meth(self):
        if self._condition:
            print('truth')

    @cached_property.cached_property
    def _condition(self):
        return bool(self.arg)


def main():
    k = Klass(1)
    k.meth()


if __name__ == '__main__':
    main()
