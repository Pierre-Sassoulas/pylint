from enum import Enum


class ABC(Enum):
    A = "A"
    B = "B"
    C = "C"


def true_positive(a: ABC):
    if a == ABC.A:
        c = "user"
    if a == ABC.B:
        c = "contributor"
    print(c)  # true positive


def false_negative(a: ABC, b: bool):
    if b:
        if a == ABC.A:
            c = "user"
        if a == ABC.B:
            c = "contributor"
    # do more stuff
    if b:
        print(c)  # false negative
