import logging
from enum import Enum


class ConstraintType(Enum):  # pylint: disable=missing-class-docstring,too-few-public-methods
    DISTANCE = 0
    FORCE = 1


constraintType = "none"

switch = {
    "distance": ConstraintType.DISTANCE,
    "force": ConstraintType.FORCE
}

if constraintType not in switch.keys():
    logging.error(f"Forgot to add a constraint type \"{constraintType}\" to the AST")
    result = None

result = switch[constraintType]
