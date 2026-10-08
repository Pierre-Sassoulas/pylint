from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class GenericModel(BaseModel, Generic[T]):
    prop1: T

class ChildModel(GenericModel[int]):
    prop2: int

print(ChildModel(prop1=1, prop2=2))
