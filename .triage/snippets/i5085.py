class Xxx:
    def __init__(self):
        self.__val = None

    @property
    def get_value(self) -> int:
        if self.__val is None:
            self.__val = 42
        return self.__val

    def method(self):
        return "qwe"[: -self.get_value]
