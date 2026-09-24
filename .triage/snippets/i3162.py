from typing import NewType


class A:
    def __init__(self, value: int):
        self.value = value


a = A(5)
print(a.value)

B = NewType("B", A)

b = B(a)
print(b.value)
