from typing import Callable
from inspect import signature


def convertToDictWithKey(func: Callable[[str], int]) -> Callable[[str, str], dict]:
    """Decorator that adds an argument and change the return type to a dict"""

    def inner(keyName: str, inStr: str) -> dict:
        return {keyName: func(inStr)}

    return inner


@convertToDictWithKey
def stringLengthWithKey(inStr: str) -> int:
    """Return the length of a string"""
    return len(inStr)


print(signature(stringLengthWithKey))  # prints (keyName: str, inStr: str) -> dict

# E1121: Too many positional arguments for function call (too-many-function-args)
# Note 1: it does not print E1136
# Note 2: it disappears with signature-mutators
print(stringLengthWithKey("myKey", "mystr")["myKey"])  # prints 5


def convertToDict(func: Callable[[str], int]) -> Callable[[str], dict]:
    """Decorator that changes the return type to a dict"""

    def inner(inStr: str) -> dict:
        return {"myKey": func(inStr)}

    return inner


@convertToDict
def stringLength(inStr: str) -> int:
    """Return the length of a string"""
    return len(inStr)


print(signature(stringLength))  # prints (inStr: str) -> dict

# E1136: Value 'stringLength('mystr')' is unsubscriptable (unsubscriptable-object)
# Note: it does not disappear with signature-mutators
print(stringLength("mystr")["myKey"])  # prints 5
