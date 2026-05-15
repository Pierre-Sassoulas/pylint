class Test:
    def test(self):
        self.__new__(type(self))
        type(self).__new__(type(self))
