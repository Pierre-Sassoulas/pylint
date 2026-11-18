"""pylint test"""

import abc


class Animal(abc.ABC):
    """Animal class"""

    @property
    def name(self) -> str:
        """Animal name"""

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, animal_dict: dict):
        """Parse an Animal object from a dict"""
        return cls()


class Dog(Animal):
    """Dog class"""

    name = "dog"
    barks = False

    @classmethod
    def from_dict(cls, animal_dict):
        new_dog = super().from_dict(animal_dict)
        new_dog.barks = animal_dict.get("barks")

        return new_dog


dog = Dog.from_dict({"barks": True})

print(dog.name)
print(dog.barks)

