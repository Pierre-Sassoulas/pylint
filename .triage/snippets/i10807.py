import typing


class A:
    def parent_meth(self) -> typing.Self:
        return self


class B(A):
    def meth(self) -> typing.Self:
        return super().parent_meth()

    def f2(self):
        pass


B().meth().f2()
