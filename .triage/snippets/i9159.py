import typing


class A:
    @classmethod
    def f1(cls) -> typing.Self:
        return cls()


class B(A):
    @classmethod
    def f1(cls) -> typing.Self:
        return super().f1()

    def f2(self):
        pass


B.f1().f2()
