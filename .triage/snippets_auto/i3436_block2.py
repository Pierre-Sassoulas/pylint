$ pylint test.py
************* Module test
test.py:5:13: C0326: No space allowed around keyword argument assignment
def test(foo = "bar"):
             ^ (bad-whitespace)
test.py:1:0: C0111: Missing module docstring (missing-docstring)
test.py:5:0: C0102: Black listed name "foo" (blacklisted-name)
test.py:5:0: C0111: Missing function docstring (missing-docstring)
test.py:3:0: W0611: Unused import json (unused-import)

--------------------------------------------------------------------
Your code has been rated at -6.67/10 (previous run: 6.67/10, -13.33)
