def f():
    yield input()


[x] = f()
if x:
    pass
