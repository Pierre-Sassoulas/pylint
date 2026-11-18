# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
# pylint: disable=pointless-statement,too-few-public-methods,unused-variable

import functools
import sys
from typing import Callable


class MyClass:
    def func(self, something: bool, something_else: bool, and_another: bool):
        callback: Callable[[str], str | None] | None = None
        if something:
            callback = self._foo
        elif something_else:
            callback = functools.partial(print, file=sys.stderr)
        elif and_another:
            callback = lambda msg: "Hello world"

        [...]  # Do something with callback

    def _foo(self, msg: str) -> str:
        [...]  # Do something interesting
        return msg.upper()

