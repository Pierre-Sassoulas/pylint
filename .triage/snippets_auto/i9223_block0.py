from typing import Callable  # unused-import

from typing_extensions import TypeAlias

MyAlias: TypeAlias = "Callable[[int, int], int]"

def my_function(_: MyAlias) -> None:
    ...

my_function(1)
