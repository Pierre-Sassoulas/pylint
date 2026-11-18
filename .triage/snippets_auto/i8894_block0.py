""" module docstring """
import pydantic.v1 as pydantic


class ClassA(pydantic.BaseModel):
    """Class A"""

    field_a : float


class ClassB(pydantic.BaseModel):
    """Class B"""

    # doesnt trigger pylint
    obj_a: ClassA

    # triggers Instance of 'FieldInfo' has no 'field_a' member (no-member) from below method
    obj_a: ClassA = pydantic.Field(...)

    def get_field_a(self):
        """Grab the 'field_a' from 'self.obj_a'."""
        return self.obj_a.field_a

# simple test to show that the method works as expected
FIELD_A = 1.0
obj_a = ClassA(field_a=FIELD_A)
obj_b = ClassB(obj_a=obj_a)
assert obj_b.get_field_a() == FIELD_A
