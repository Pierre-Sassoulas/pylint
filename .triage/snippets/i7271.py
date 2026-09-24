import asyncio


async def main():
    async def my_gen():
        for _ in range(10):
            yield _

    result = tuple([_ async for _ in my_gen()])
    print(result)


asyncio.run(main())
