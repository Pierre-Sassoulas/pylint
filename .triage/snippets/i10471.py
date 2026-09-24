from abc import ABC, abstractmethod


class CallableBase(ABC):
    @abstractmethod
    def __call__(self, data: str) -> str: ...


class ConcreteCallable(CallableBase):
    def __call__(self, data: str) -> str:
        return f"processed: {data}"


class Container:
    def __init__(self, processor: CallableBase | None = None):
        self.__processor = processor

    @property
    def processor(self) -> CallableBase | None:
        return self.__processor

    def process_with_property(self, data: str) -> str:
        if self.processor:
            return self.processor(data)
        return data
