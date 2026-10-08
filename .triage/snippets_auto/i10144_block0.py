"""hi.py file."""
from pydantic import BaseModel


class Person(BaseModel):
    """This is a person class."""

    name: str
    age: int


if __name__ == '__main__':
    p = Person(name='John Doe', age=30)
    print(p)

    print("model fields via class variable:")
    print("Pylint will error on this when it shouldn't")
    for field in Person.model_fields:
        print(field)

    print("model fields via instance variable:")
    print("Pylint does not error on this")
    for field in p.model_fields:
        print(field)
