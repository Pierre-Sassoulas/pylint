from __future__ import annotations
from typing import Annotated, TypeAlias

Seconds: TypeAlias = Annotated[float, "seconds"]
DAY: Annotated[Seconds, "number of seconds in a day"] = 86400
