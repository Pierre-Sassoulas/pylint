#! /usr/bin/env python3
# pylint: disable=missing-docstring

def some_func():
    var = 3
    print(var)
    var = 4
    # var is never used again. The last assignment thus could be removed.
