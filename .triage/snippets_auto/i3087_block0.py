foo = collections.namedtuple("foo", "")

def bar() -> foo # Here pylint warns me
    global foo
    foo = collections.namedtuple("foo", "a b")
    return foo
