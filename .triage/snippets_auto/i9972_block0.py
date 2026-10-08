
from dataclasses import dataclass, field

def field_alias(**kwargs):
    # do some stuff analyzing the args

    # The following ignore is "fine" because it only needs to happen in one spot
    return field(**kwargs)  # pylint: disable=invalid-field-call

class ObjectWSubField:
    sub_field: int

@dataclass(frozen=True)
class Temp:
    the_object: ObjectWSubField = field_alias(type=ObjectWSubField)

    def some_method(self):
        # no-member error thrown here and I don't want to throw in an ignore at every spot
        print(self.the_object.sub_field)
