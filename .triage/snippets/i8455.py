from typing import TypeAlias

DictAlias: TypeAlias = dict[int, float]
assert DictAlias.__origin__ is dict
