# pylint: disable=consider-using-f-string,missing-module-docstring
WORD = "abc"
print("%d" % "abc")  # works
print("%d %d" % (WORD, 1))  # works
print("%d", WORD)  # doesn't work
print("{:d}".format("abc"))  # doesn't work
print(f"{'abc':d}")  #  doesn't work
