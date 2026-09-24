from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def do_something(self):
        pass


class Derived(Base):
    def do_something_else(self):
        pass
