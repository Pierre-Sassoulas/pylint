from __future__ import annotations


def foo():
    class Foo:
        def foo(self) -> Foo: ...


class Bar:
    def foo(self) -> Bar: ...
