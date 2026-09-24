import re
from dataclasses import dataclass


@dataclass
class _Test:
    pattern_instance: re.Pattern[str]


C = _Test(pattern_instance=re.compile(r"regex pattern"))
print(C.pattern_instance.pattern)
