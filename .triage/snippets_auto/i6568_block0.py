"""
Module doc string
"""

from enum import Enum


def module_function():  # should reject
    pass


def moduleFunction():  # should be OK
    pass


def ModuleFunction():  # should reject
    pass


class SampleEnum(Enum):
    """
    Sample Enum
    """
    CAPS_CASE = 0  # should be OK

    snake_case = 1  # should reject
    _snake_case = 2  # should reject
    __snake_case = 3  # should reject

    camelCase = 4  # should reject
    _camelCase = 5  # should reject
    __camelCase = 6  # should reject

    PascalCase = 7  # should reject
    _PascalCase = 8  # should reject
    __PascalCase = 9  # should reject


class CaseTestClass:
    """
    case testing
    """
    # class-attribute-naming-style=PascalCase all others should be rejected
    class_attr_snake_case = 0  # should reject
    _class_attr_snake_case = 0  # should reject
    __class_attr_snake_case = 0  # should reject

    classAttrCamelCase = 0  # should reject
    _classAttrCamelCase = 0  # should reject - ERROR: this is "protected" class attribute in camelCase instead of PascalCase
    __classAttrCamelCase = 0  # should reject

    ClassAttrPascalCase = 0  # should be OK
    _ClassAttrPascalCase = 0  # should be OK
    __ClassAttrPascalCase = 0  # should be OK - ERROR: this is private class attribute in PascalCase it should be ok but generates invalid-name

    # there is no specific styling for "class methods" so assume "method" styling applies
    # method-naming-style=camelCase
    @classmethod
    def class_method_snake_case(cls):  # should reject
        pass

    @classmethod
    def _class_method_snake_case(cls):  # should reject
        pass

    @classmethod
    def __class_method_snake_case(cls):  # should reject
        pass

    @classmethod
    def classMethodCamelCase(cls):  # should be OK
        pass

    @classmethod
    def _classMethodCamelCase(cls):  # should be OK
        pass

    @classmethod
    def __classMethodCamelCase(cls):  # should be OK - ERROR: this is private class method in camelCase - should be OK but generates invalid-name
        pass

    @classmethod
    def ClassMethodPascalCase(cls):  # should reject
        pass

    @classmethod
    def _ClassMethodPascalCase(cls):  # should reject - ERROR: this is "protected" method in PascalCase - it should be rejected
        pass

    @classmethod
    def __ClassMethodPascalCase(cls):  # should reject
        pass

    def __init__(self) -> None:
        super().__init__()
        self.snake_case_attr = 0  # should be OK
        self._snake_case_attr = 0  # should be OK
        self.__snake_case_attr = 0  # should be OK

        self.camelCaseAttr = 0  # should reject
        self._camelCaseAttr = 0  # should reject
        self.__camelCaseAttr = 0  # should reject

        self.PascalCaseAttr = 0  # should reject
        self._PascalCaseAttr = 0  # should reject
        self.__PascalCaseAttr = 0  # should reject

    def snake_case_method(self):  # should reject

        # use attributes to avoid "unused <>" warnings
        print(self.__snake_case_attr)
        print(self.__camelCaseAttr)
        print(self.__PascalCaseAttr)

        CaseTestClass.__class_method_snake_case()
        CaseTestClass.__classMethodCamelCase()
        CaseTestClass.__ClassMethodPascalCase()

        self.__snake_case_method()
        self.__camelCaseMethod()
        self.__PascalCaseMethod()

    def _snake_case_method(self):  # should reject
        pass

    def __snake_case_method(self):  # should reject
        pass

    def camelCaseMethod(self):  # should be OK
        pass

    def _camelCaseMethod(self):  # should be OK
        pass

    def __camelCaseMethod(self):  # should be OK - ERROR: this is private method in camelCase should be OK but generates invalid-name
        pass

    def PascalCaseMethod(self):  # should reject
        pass

    def _PascalCaseMethod(self):  # should reject - ERROR: this is "protected" method in PascalCase should be rejected but it is not
        pass

    def __PascalCaseMethod(self):  # should reject
        pass

