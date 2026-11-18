from abc import ABCMeta, abstractmethod
import asyncio
from contextlib import AbstractAsyncContextManager, asynccontextmanager

class Base(metaclass=ABCMeta):
    @abstractmethod
    def get(self) -> AbstractAsyncContextManager[str]:
        pass

class Implementation(Base):
    @asynccontextmanager
    async def get(self):
        yield "hello"

async def main():
    async with Implementation().get() as res:
        print(res)

if __name__ == "__main__":
    asyncio.run(main())
