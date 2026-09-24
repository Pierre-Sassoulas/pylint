import sys

if sys.version_info > (2,):
    from collections.abc import Set
else:
    from collections.abc import Set

isinstance(set(), Set)
