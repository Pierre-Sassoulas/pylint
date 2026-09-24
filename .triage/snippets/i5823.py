from dataclasses import dataclass


@dataclass(slots=True)
class _Animal:
    name: str
    num_arms: int
    num_legs: int

    def greet(self):
        print(f"Hi, my name is {self.name}")


@dataclass(slots=True)
class Bird(_Animal):
    num_arms: int = 0
    num_legs: int = 2

    def greet(self):
        print("Chirp!")
        super().greet()
