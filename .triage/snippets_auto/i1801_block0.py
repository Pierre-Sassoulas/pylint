'''
Example demonstrating a false-positive of the 'no-value-for-parameter' error
in pylint.
'''

from enum import Enum


class EnumWithDoc(Enum):
    '''
    See https://docs.python.org/3/library/enum.html#using-a-custom-new
    '''

    def __new__(cls, value, doc):
        obj = object.__new__(cls)
        obj._value_ = value  # <-- False warning reported here
        obj.doc = doc
        return obj


class Example(EnumWithDoc):
    '''
    Example enum using the "EnumWithDoc" class.
    '''

    A = (1, 'The first value')
    B = (2, 'The second value')


def main():
    '''
    Main method
    '''

    my_value = Example(1)  # <-- False error reported here!
    print(repr(my_value))
    print(my_value.doc)


main()
