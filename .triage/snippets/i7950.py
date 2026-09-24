import abc
import unittest


class Abstract(unittest.TestCase, abc.ABC):
    @abc.abstractmethod
    def test_something(self):
        pass

    @abc.abstractmethod
    def test_another_thing(self):
        pass


class AbsSub(Abstract, abc.ABC):
    def test_another_thing(self):
        return 1


class Sub(AbsSub):
    pass
