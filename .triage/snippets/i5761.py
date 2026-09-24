from collections.abc import AsyncIterable
from typing import Protocol


class Foo(Protocol):
    def bar(self) -> AsyncIterable[str]: ...


class Foo2(Foo):
    async def bar(self) -> AsyncIterable[str]:
        yield "hello"
