"""A test case."""
import numpy as np

class Foo:
    """Class docstring."""

    csvfilename = None
    csvdata = None

    def __init__(self, filename):
        cls = self.__class__
        assert filename is not None
        if cls.csvfilename != filename:
            cls.csvdata = np.zeros(10)
            cls.csvfilenanme = filename
        self.generation = cls.csvdata[0]
