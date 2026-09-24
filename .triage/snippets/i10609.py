from enum import Enum


class CustomEnum(Enum):
    pass


MyEnum = CustomEnum("MyEnum", {"RED": 1})
MyEnum2 = Enum("MyEnum2", {"BLUE": 2})


class MyEnum3(CustomEnum):
    GREEN = 3
