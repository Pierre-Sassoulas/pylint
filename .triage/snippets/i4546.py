def foo(arg):
    print(arg)


def returns_implicit_tuple(x):
    return (x,)


args = list(returns_implicit_tuple(1))
foo(*args)
