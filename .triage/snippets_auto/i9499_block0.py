from dataclasses import dataclass

@dataclass
class MyClass:
    __slots__ = ('foo', 'bar', )
    foo: str

    def __init__(self):
        self.foo = 'one'
        self.bar = 'two'
