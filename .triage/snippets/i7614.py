def foo(a=None, b=None, c=None):
    pass


d = {"a": 1, "b": 2, "c": 3}

x = d.pop("c")

foo(c=x, **d)
