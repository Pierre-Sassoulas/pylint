""" Description of the module. """

from enum import Enum
from typing import Union


class SomeEnum(Enum):
    """ Enum description. """
    MEMBER_1 = 'value 1'
    MEMBER_2 = 'value 2'


class SomeClass:
    """ Class description. """

    def __init__(self) -> None:
        self.name: str = 'lorem ipsum'

    def too_few_public_methods(self) -> str:
        """ Function description.

        :return: A description of the return value.
        :rtype: str
        """
        return self.name

    def test_function(self, name: Union[str, SomeEnum]) -> bool:
        """ Function description.

        :param Union[str, SomeEnum] name: The description of the input variable.
        :return: A description of the return value.
        :rtype: bool
        """
        return name == self.name
