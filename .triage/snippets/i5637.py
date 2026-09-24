from typing import TYPE_CHECKING


class Foo:
    if TYPE_CHECKING:

        def __init__(self) -> None:
            pass

    else:

        def __init__(self, value: int) -> None:
            pass


a = Foo()
