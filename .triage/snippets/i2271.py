from functools import partial


def foo(x, y):
    return (x, y)


bar_module = partial(foo, "")


class A:
    bar = bar_module

    def b(self):
        y = 1
        self.bar(y=y)
