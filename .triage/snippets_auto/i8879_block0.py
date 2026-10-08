
"""
This class shows a bug in pylint.
"""


class Base:
    """
    This is where the invalid-name field is defined.
    """

    # pylint: disable=invalid-name
    thisIsABadField: str
    # pylint: enable=invalid-name

    def __init__(self, greeting: str):
        print(greeting)

    def do_something(self):
        self.thisIsABadField = "hello"

    def do_another(self):
        self.thisIsABadField = "hello again"
