# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,too-few-public-methods
class Parent:
    def __init__(self):
        self._foo = 1

    @classmethod
    def create_instance(cls):
        return cls()

class Child(Parent):
    def __init__(self):
        super().__init__()
        self._bar = 'a'

    @classmethod
    def create_instance(cls):
        inst = super().create_instance()
        inst._foo = 2   # protected-access warning here
        inst._bar = 'b' # protected-access warning here

    @classmethod
    def create_instance2(cls):
        inst = cls()
        inst._foo = 3   # no warning here thanks to #4267
        inst._bar = 'c' # no warning here thanks to #4267

    def get_var(self):
        return self._foo # no warning here
