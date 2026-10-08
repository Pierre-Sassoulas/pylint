"""test_lint.py"""
from typing import Optional

class Foo:
    """class Foo"""
    a: Optional[dict] = None
    def empty(self):
        """foo"""

    @classmethod
    def init(cls):
        """init"""
        if cls.a is None:
            cls.a = {}
        assert cls.a is not None
        assert isinstance(cls.a, dict)
        if cls.a is None:
            return
        cls.a[1] = 2
        _ = cls.a[1]
        _ = 1 in cls.a
