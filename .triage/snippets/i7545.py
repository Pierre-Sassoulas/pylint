import contextlib


@contextlib.contextmanager
def f():
    yield ("A", "B")


@contextlib.contextmanager
def g(_):
    yield "C"


with f() as (a, b), g(a) as c:
    pass
