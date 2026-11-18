# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods

class Super:
    def __init__(self):
        pass


class Sub(Super):
    def __init__(self):
        super().__init__()
        self.some_value = 0


def get_super(x: bool) -> Super:
    if x:
        return Sub()
    return Super()


obj = get_super(True)
assert isinstance(obj, Sub)
obj.some_value = 27
