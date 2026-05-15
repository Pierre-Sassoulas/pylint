import enum


class Thing(enum.Enum):
    A = enum.auto()

    @property
    def value(self):
        return "thing"
