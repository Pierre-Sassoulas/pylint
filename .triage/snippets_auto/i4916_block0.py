from abc import abstractmethod


class ParentA:
    """Parent class A."""


class ChildA(ParentA):
    """Child class A."""


class ParentB:
    """Parent class B: can be concrete or abstract class."""

    def __init__(self):
        self._attr: ParentA = ParentA()

    @abstractmethod
    def attr(self) -> ParentA:
        """Return the attribute.

        Returns
        -------
        ParentA
            The attribute attr
        """
        raise NotImplementedError


class ChildB(ParentB):
    """Concrete class ChildB."""

    def __init__(self):
        self._attr: ChildA = ChildA()

    def attr(self) -> ChildA:
        # Pylint will not raise any warning here because docstring of ParentB.attr exists
        return self._attr
