import asyncio

from pydantic import BaseModel, PrivateAttr


class SomeModel(BaseModel):
    _some_lock: asyncio.Lock = PrivateAttr(default_factory=asyncio.Lock)

    async def some_method(self) -> None:
        async with self._some_lock:
            await asyncio.sleep(1)


model = SomeModel()
asyncio.run(model.some_method())
