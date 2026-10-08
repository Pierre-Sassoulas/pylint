from pydantic import Field
from pydantic.dataclasses import dataclass

@dataclass
class Example:
    number: int = Field(alias='n')


example = Example(n=5)
