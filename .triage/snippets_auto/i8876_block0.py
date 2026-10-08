# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


class Foo(tuple):

    def __new__(cls, iterable) -> 'Foo':
        instance = super().__new__(cls, iterable)

        instance._x = 0
        instance.y = 1
        return instance

    @property
    def x(self):
        return self._x


my_foo = Foo(("c", "b", "a"))
print(my_foo.x, my_foo.y)


class Bar(tuple):

    def __new__(cls, iterable) -> 'Bar':
        instance = super().__new__(cls, sorted(iterable))

        instance._x = 0
        instance.y = 1
        return instance

    @property
    def x(self):
        return self._x


my_bar = Bar(("c", "b", "a"))
print(my_bar.x, my_bar.y)

