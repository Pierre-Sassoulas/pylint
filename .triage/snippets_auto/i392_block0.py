# ==> db.py <==
class Users(object):
    __slots__ = ['name', '_name']

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    name = property(get_name, set_name, None, "The name property")

    @staticmethod
    def findByName(unused_name):
        return Users("test user")

    def __init__(self, value="Unknown"):
        self._name = value

# ==> test.py <==
from db import Users


def test():
    user = Users.findByName("foo")
    user.namea = "typo in the field name"
    print user.name
    print user._name

test()
