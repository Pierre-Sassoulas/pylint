import os
from dataclasses import dataclass


@dataclass
class EnvVar:
    name: str
    _initial_value: str | None = None

    def __post_init__(self):
        self._initial_value = os.getenv(self.name)
