from collections.abc import AsyncIterator


async def gen() -> AsyncIterator[int]:
    yield 1


async def use():
    async for x in gen():
        print(x)
