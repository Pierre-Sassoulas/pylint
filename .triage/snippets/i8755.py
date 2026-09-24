class C:
    pass


@classmethod
def foo(cls, a):
    b = super(C, cls).foo(a)
    return b
