class my_prop(property):
    pass


class my_prop2(my_prop):
    pass


class Test:
    def __init__(self) -> None:
        self._prop = None
        self._prop2 = None

    @my_prop
    def prop(self) -> str:
        return self._prop

    @my_prop2
    def prop2(self) -> str:
        return self._prop2


c = Test()

if c.prop == "test":
    pass

if c.prop2 == "test":
    pass
