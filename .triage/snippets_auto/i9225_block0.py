from typing import Protocol

class TestProto(Protocol):
    """Note that there's no __init__ method here"""

class Test1(TestProto):
    """Note that there's no __init__ method here"""

class Test2(Test1):
    """Inherit explicitly from Test1"""

    def __init__(self):
        """Initialize this object"""
