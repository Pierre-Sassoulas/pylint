import dataclasses
from typing import Optional

FILENAME = "test_two.py"


@dataclasses.dataclass
class IOArgs:
    """Dataclass storing information about how to open a file"""

    encoding: Optional[str]
    mode: str


args_good_one = IOArgs(encoding=None, mode="wb")
args_good_two = IOArgs(encoding="utf8", mode="w")
args_bad_one = IOArgs(encoding=None, mode="w")
LOCALE_ENCODING = None
args_bad_two = IOArgs(encoding=LOCALE_ENCODING, mode="w")

file = open(FILENAME, args_good_one.mode, encoding=args_good_one.encoding)
file = open(FILENAME, args_good_two.mode, encoding=args_good_two.encoding)
file = open(FILENAME, args_bad_one.mode, encoding=args_bad_one.encoding)
file = open(FILENAME, args_bad_two.mode, encoding=args_bad_two.encoding)
