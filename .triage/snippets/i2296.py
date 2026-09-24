from typing import NewType

a = NewType("a", list[int])


def fun() -> a:
    data = [1, 2, 3]
    return a(data)


def fun1():
    for x in fun():
        pass
