class X:
    def __init__(self, f=None):
        self.f1, self.f2 = f or (None, None)

    def g(self, x):
        if self.f1:
            return self.f1(x)
        return x

    def h(self, y):
        return self.f2(y) if self.f2 else y
