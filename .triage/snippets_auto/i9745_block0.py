from asyncio import sleep
from typing import Any, Awaitable, Coroutine


class A:
    async def fun(self) -> None:
        pass


class B(A):
    def fun(self) -> Awaitable[None]:
        return sleep(42)


class C(A):
    def fun(self) -> Coroutine[Any, Any, None]:
        return sleep(42)
