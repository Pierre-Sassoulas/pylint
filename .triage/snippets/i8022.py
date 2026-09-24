from typing import Generic, TypeVar

T = TypeVar("T")


class WrappedVal(Generic[T]):
    def __init__(self, value: T):
        self._value = value

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, x: T):
        self._value = x


val1 = WrappedVal("hello")
val1.value = "goodbye"

val2 = WrappedVal(1.0)
print(-val2.value)
