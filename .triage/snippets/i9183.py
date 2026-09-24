from dataclasses import dataclass


@dataclass
class Youpi:
    yapi: int


print(Youpi.__dataclass_fields__)
