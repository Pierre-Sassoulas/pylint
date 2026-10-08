# ==> db.py <==
class Users(object):
    ....    
    @staticmethod
    def findByName(unused_name):
        results = []
        for unused in xrange(10):
            results.append(Users("test user"))
        return results

    def __init__(self, value="Unknown"):
        self._name = value

# ==> test.py <==
from db import Users


def test():
    for user in Users.findByName("foo"):
        user.namea = 1
        print user.name
        print user._name

test()
