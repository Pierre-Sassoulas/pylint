TEST = 1

def foo1(spam=(TEST == 0)):  # superfluous-parens
    return spam


def foo2(spam=TEST == 0):  # unreadable
    return spam


def foo3(spam= TEST == 0):  # only slightly better, but it's not PEP 8
    return spam


def foo4(spam= TEST == ((3 + 2))):  # but here we want C0325!
    return spam
