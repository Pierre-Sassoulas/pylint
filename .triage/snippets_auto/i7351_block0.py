# pylint: disable=missing-module-docstring, disable=missing-class-docstring

from unittest import TestCase
from unittest.mock import MagicMock, call, patch


class HasDunder:  # pylint: disable=too-few-public-methods
    def __setitem__(self, key: int, value: int) -> None:
        pass


class TestClass(TestCase):
    def test___setitem__(self) -> None:  # pylint: disable=missing-function-docstring
        all_mocks = MagicMock()

        has_dunder = HasDunder()
        with patch.object(HasDunder, "__setitem__") as mock__setitem__:
            all_mocks.attach_mock(mock__setitem__, "HasDunder.__setitem__")
            has_dunder[1] = 2
        all_mocks.assert_has_calls([call.HasDunder.__setitem__(1, 2)])
