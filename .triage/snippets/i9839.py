import enum


class Priority(enum.IntEnum):
    __slots__ = ()

    LOW = enum.auto()
    MEDIUM = enum.auto()
    HIGH = enum.auto()
    CRITICAL = enum.auto()
