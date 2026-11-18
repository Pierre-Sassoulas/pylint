class A:
    def get_stuff(self, x):
        return x


def test1():
    def g():
        pass
    a = A()
    a.get_stuff = g


def test2():
    a = A()
    value = a.get_stuff(1)
