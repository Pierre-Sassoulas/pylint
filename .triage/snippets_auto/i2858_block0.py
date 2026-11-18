from typing import NamedTuple

class Car(NamedTuple):
    color: str
    mileage: float
    automatic: bool

car1 = Car('red', 3812.3, True)
car1.mileage = 12
