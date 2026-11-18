import pytest

def apparently_inconsistent_returning_function(return_something: bool) -> None:
    """A function that looks like not all paths return something."""
    if return_something:
        return None
    pytest.exit("Raises an exception.")
