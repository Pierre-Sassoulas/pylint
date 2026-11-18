# pylint: disable=missing-docstring,too-few-public-methods

import ctypes

class Test(ctypes.Structure):
    _fields_ = [("member", ctypes.c_uint8)]

test = Test()
test.member = 42
# pylint: disable=attribute-defined-outside-init
test.not_a_member = 24
assert bytes(test) == b"\x2A"
