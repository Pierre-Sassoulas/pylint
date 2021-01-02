# pylint: disable=invalid-name,missing-module-docstring
import circular_import_b as b  # [cyclic-import]

print(b)
