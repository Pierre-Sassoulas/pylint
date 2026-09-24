class A:
    @property
    def x(self):
        raise NotImplementedError


class B(A):
    @x.getter
    def x(self):
        return 42
