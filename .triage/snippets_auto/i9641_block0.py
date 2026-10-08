"""The following code should lint ok, but pylint issues undefined- / unused-variable l"""
import pytest


@pytest.mark.parametrize("x", l := [1, 2, 3])
@pytest.mark.parametrize("y", l)
def test_demo(x, y):
    """pylint demo"""
    _ = [x, y]
