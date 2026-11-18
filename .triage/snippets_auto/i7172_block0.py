# pylint: disable=C0116,C0114,C0303,C0115,R0903
class Duff:
    def __init__(self):
        self._duff = None

    @property
    def duff(self):
        return self._duff

    @duff.setter
    def duff(self, value):
        self._duff = value

class DuffPlusOne(Duff):
    
    def __init__(self):
        super().__init__()
        self._duff = None

    @duff.setter
    def duff(self, value):
        self._duff = value + 1
