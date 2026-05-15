class Foo:
    def method(self):
        pass


class Bar(Foo):
    def method(self, param):
        pass


class TestOne:
    def test(self):
        foo = Foo()
        foo.method = lambda x: x


class TestTwo:
    def test(self):
        bar = Bar()
        bar.method(param=1)
