from typing import Literal, NoReturn, overload

@overload
def pick(kind: Literal["apple"]) -> str: ...
@overload
def pick(kind: None) -> NoReturn: ...
def pick(kind):
    if kind is None:
        raise ValueError
    return kind
