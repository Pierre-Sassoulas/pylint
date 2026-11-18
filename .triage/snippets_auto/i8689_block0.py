"""Repro for issue that burned time due to 'missing arguments'.
Context: The original issue came from some async sqlalchemy fun, where the
'cake_type' was a DeclarativeBase type.
"""
# pylint: disable=too-few-public-methods
from typing import Any, Callable, TYPE_CHECKING


if TYPE_CHECKING:
    from typing_extensions import ParamSpec, TypeVar
    Params = ParamSpec('Params')
    Sometype = TypeVar('Sometype')


def add_an_arg(func: "Callable[..., Sometype]"):
    """Mutate a function, that's always fun."""
    def wrapper(self: "Base", *args: "Params.args",
                **kwargs: "Params.kwargs") -> "Sometype":
        return func(self, 'hello', *args, **kwargs)
    return wrapper


class CheeseCake:
    """A good cake."""


class Base:
    """Base repro class."""
    def __init__(self, cake_type: Any):
        self.cake_type = cake_type

    @add_an_arg
    def say_something_and_serve_cake(self, hello_arg: str, something_else: int):
        """Say something n times and return a cake."""
        for _ in range(something_else):
            print(hello_arg)
        return self.cake_type()


class CheesecakePlace(Base):
    """The subclass where the pain happens."""
    def __init__(self):
        super().__init__(CheeseCake)

    def new_customers_enter(self, num_customers: int):
        """Do the usual stuff when a new customer enters."""
        self.say_something_and_serve_cake(num_customers)

    if TYPE_CHECKING:
        def say_something_and_serve_cake(
            self, hello_arg: str, something_else: int,
        ) -> CheeseCake:
            ...
