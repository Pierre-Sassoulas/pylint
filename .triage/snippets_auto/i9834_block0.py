"""
The following code should lint without errors, but pylint shows:
test.py:14:8: E1101: Instance of 'A' has no 'y' member (no-member)
"""
# pylint: disable=too-few-public-methods, pointless-statement


class A:
    """dummy class"""


a = A()
if a.x or \
        a.y:  # pylint: disable=no-member
    pass
