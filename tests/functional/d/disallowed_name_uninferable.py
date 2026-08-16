"""Checking a name against ``bad-names`` does not need the assigned value."""
from unknown_pkg import mystery  # pylint: disable=import-error

# The value cannot be inferred, so there is no naming style to check the name
# against, but the blocklist does not depend on one.
foo = mystery()  # [disallowed-name]

# Reassigning makes the value ambiguous rather than unknown; same conclusion.
BANANA = 1  # [disallowed-name]
BANANA = mystery()  # [disallowed-name]

print(foo, BANANA)
