class Base:
    def __init__(self) -> None:
        self.__foobar = "foobar"


class Derived(Base):
    def do_it(self) -> None:
        print(self.__foobar)


o = Derived()
o.do_it()
