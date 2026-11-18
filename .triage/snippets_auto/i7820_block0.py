"Demonstrate class property problems"

from typing import Callable

class ClassROProperty(property):
    "Decorator class to create a read-only class property"
    def __init__(self, getter:Callable):
        self._getter = getter

    def __get__(self, _, cls):
        return self._getter(cls)

class MyClass:
    "A class which has only class properties"

    @ClassROProperty
    def prop_1(cls):
        "Return an iterable value"
        return [1, 2, 3, 4]

for val in MyClass.prop_1:
    print(val)
print(MyClass.prop_1[1])
