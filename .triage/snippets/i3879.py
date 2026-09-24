class Test:
    def __init__(self):
        self.__test = "test"


class TestSub(Test):
    def __init__(self):
        Test.__init__(self)


print(TestSub()._Test__test)
