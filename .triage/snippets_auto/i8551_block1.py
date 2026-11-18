"""a.py"""

# pylint: disable=missing-function-docstring

from unittest.mock import MagicMock, call, patch

from .b import some_context_manager  # pylint: disable=relative-beyond-top-level

def just_enters() -> None:
    # NOTE: the pylint false positive is on the next line: unnecessary-dunder-call
    some_context_manager().__enter__()

@patch(f"{__name__}.some_context_manager")
def test_just_enters(mock_some_context_manager: MagicMock) -> None:
    all_mocks = MagicMock()
    all_mocks.attach_mock(mock_some_context_manager, "some_context_manager")

    just_enters()

    # Known pylint bug, SEE: https://github.com/pylint-dev/pylint/issues/7351
    # pylint: disable-next=unnecessary-dunder-call
    all_mocks.assert_has_calls([call.some_context_manager().__enter__()])
