from typing import NewType

MyTuple = NewType("T", tuple[float, float])
x = MyTuple((1.1, 2.2))
x[0]
