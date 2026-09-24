from typing import TYPE_CHECKING, Any, TypeVar

_T = TypeVar("_T", bound=Any)


class myfunc:
    def __init__(self, *args: Any) -> None:
        pass


class _FunctionGenerator:
    if TYPE_CHECKING:

        @property
        def myfunc(self) -> type[myfunc]: ...


func = _FunctionGenerator()

func.myfunc(1, 2, 3)
