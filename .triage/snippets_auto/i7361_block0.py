# pylint: disable=missing-module-docstring, too-few-public-methods, missing-class-docstring
# pylint: disable=missing-function-docstring
class SomeParent:
    def __init__(self):
        self.some_variable = {}

    def get_some_variable(self):
        return "some-variable"


class SomeChild(SomeParent):
    def __init__(self):
        super().__init__()
        self.some_other_variable = {}
