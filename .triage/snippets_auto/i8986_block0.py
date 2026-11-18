# pylint: disable=too-few-public-methods, missing-docstring

class Base:
    def __init__(self, config):
        print("Base.__init__")
        self.config = config


class Derived(Base):
    # This should trigger invalid-name and arguments-renamed
    def __init__(self, c):
        super().__init__(c)
        print("Derived.__init__")

