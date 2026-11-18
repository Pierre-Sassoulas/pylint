# pylint: disable=multiple-statements
from abc import ABC, abstractmethod
# All these classes have enough public methods according to pylint:

class Test:
    def __init__(self) -> None: self._field = 1
    def __getitem__(self, key: str) -> int: return self._field
    def method1(self) -> None: print(self._field)

class MyABC1(ABC):
    def __init__(self) -> None: self._field = 1
    def getitem(self) -> int: return self._field
    @abstractmethod
    def method1(self) -> None: ...

class MyABC2(ABC):
    def __init__(self) -> None: self._field = 1
    def __getitem__(self, key: str) -> int: return self._field
    @abstractmethod
    def method1(self) -> None: ...

class Concrete1(MyABC1):
    def method1(self) -> None: print("method1", self._field)

# but not this class
class Concrete2(MyABC2): # ← Too few public methods (1/2)
    def method1(self) -> None: print("method1", self._field)
