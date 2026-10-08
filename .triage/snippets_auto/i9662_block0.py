# pylint: disable=missing-module-docstring,invalid-name
a = bool(input())
b = bool(input())

if a:
    c = 123

if a and b:
    print(c)  # report possibly-used-before-assignment

if a:
    c += 1  # ok
