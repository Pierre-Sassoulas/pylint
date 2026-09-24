import datetime
from typing import Self


class MyDateTime(datetime.datetime):
    def __new__(
        cls,
        firstArg: object,
        month: int | None = None,
        day: int | None = None,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
    ) -> Self:
        return super().__new__(
            cls, firstArg, month, day, hour, minute, second, microsecond
        )
