"""Names imposed by a parent class are still checked against ``bad-names``.

Redefining an inherited name cannot rename it, so the naming style is not
checked, but a name the user blocklisted is reported wherever it appears.
"""


class Fruit:  # pylint: disable=too-few-public-methods
    """Base class spelling the names."""

    toto = 1  # [disallowed-name]

    def __init__(self):
        self.bar = 1  # [disallowed-name]

    def foo(self):  # [disallowed-name]
        """A method the child overrides."""


class Apple(Fruit):  # pylint: disable=too-few-public-methods
    """Child redefining every one of them."""

    toto = 2  # [disallowed-name]

    def __init__(self):
        super().__init__()
        self.bar = 2  # [disallowed-name]

    def foo(self):  # [disallowed-name]
        """Overrides Fruit.foo."""
