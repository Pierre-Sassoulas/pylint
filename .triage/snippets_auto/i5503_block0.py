# pylint: disable=no-self-use

class Parent:
    def func(self) -> int | None:
        return None

    def serialize(self) -> str:
        x = self.func()  # assignment-from-none
        return f"Result: {x if x else ''}"

class Child(Parent):
    def func(self) -> int:
        return 42
