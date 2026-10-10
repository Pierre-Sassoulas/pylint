import dataclasses
import datetime
import enum
from collections.abc import Callable

@dataclasses.dataclass(frozen=True)
class Payload:
    formatter: Callable[[datetime.date], str]

def format_date(value: datetime.date) -> str:
    return value.isoformat()

class FormatBase(enum.Enum):
    _value_: Payload

    def __call__(self, value: datetime.date) -> str:
        return self._value_.formatter(value)

class Format(FormatBase):
    _value_: Payload
    DEFAULT = Payload(formatter=format_date)
