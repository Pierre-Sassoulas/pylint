class MetaDang(type):
    @staticmethod
    def foo(fn, string):
        fn(string)

    def bar(cls, string):
        cls.foo(print, string)

    def baz(cls):
        cls.bar("woo")


class Dang(metaclass=MetaDang):
    pass


Dang.baz()
