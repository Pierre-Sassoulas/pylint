from typing import Generic, TypeVar

T = TypeVar("T")


class Test(Generic[T]):
    def __class_getitem__(cls, *args):
        return super().__class_getitem__(*args)

    def __init__(self, iterable):
        super().__init__()
        self._list: list[T] = list(iterable)

    def __getitem__(self, index):
        return self._list[index]


t = Test[int]([1, 2, 3])
print(t[1])
