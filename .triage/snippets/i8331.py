import typing as _t

NumericType = _t.Union[int, float, complex]
InstantiatableType = _t.Union[NumericType, str, set, None]


def instantiate(type_: str) -> InstantiatableType:
    if type_ == "int":
        return 1
    if type_ == "float":
        return 1.0
    if type_ == "complex":
        return 1.0j
    if type_ == "str":
        return "a"
    if type_ == "set":
        return set()
    return None


def negate(type_: str) -> NumericType:
    operand: InstantiatableType = instantiate(type_)

    if not isinstance(operand, (int, float, complex)):
        raise ValueError("operand not a number")

    return -operand
