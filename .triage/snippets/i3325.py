class Mine:
    def __init__(self, value: int):
        self.value = value

    def get_value(self) -> int:
        return self._value

    def set_value(self, value: int) -> None:
        self._value = value

    value = property(get_value, set_value)
