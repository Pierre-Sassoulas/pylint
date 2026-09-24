class Base:
    def fun(self, var: int) -> int:
        print(var)


class Class(Base):
    def fun(self, *, var: int) -> int:
        print(var)
