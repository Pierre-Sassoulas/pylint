import asyncio

async def nested() -> None:
    print("first()")

async def fn() -> None:
    nested()  # <-  could this issue a warning please
    await asyncio.create_task(nested())
    await asyncio.gather(nested())
    await asyncio.ensure_future(nested())

async def main() -> None:
    await fn()

asyncio.run(main())
