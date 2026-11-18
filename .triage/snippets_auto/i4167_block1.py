import pytest

def pytest_exit(*args, **kwargs):
    """Call pytest.exit."""
    pytest.exit(*args, **kwargs)

def apparently_inconsistent_returning_function(return_something: bool) -> None:
    """A function that looks like not all paths return something."""
    if return_something:
        return None
    pytest_exit("Raises an exception.")
