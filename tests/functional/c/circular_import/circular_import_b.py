# pylint: disable=invalid-name,missing-module-docstring
import circular_import_a as a # [cyclic-import]

print(a)
