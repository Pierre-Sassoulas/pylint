from abc import ABC, abstractmethod


class Animal(ABC):
    @abstractmethod
    def speak(self): ...


class Cat(Animal):  # W0223 since 4.1, silent in 4.0
    def eat(self): ...


class Tiger(Cat):
    def speak(self): ...


Tiger()  # fine
Cat()    # E0110 abstract-class-instantiated, in 4.0 and 4.1
