class Thing:
    def __init__(self, thing_type: type):
        self._type = thing_type
        self._value = None

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self._type(value)
