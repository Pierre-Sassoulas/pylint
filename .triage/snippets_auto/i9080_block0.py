from dataclasses import dataclass
from typing import Protocol

class Blah(Protocol):
    def do_thing(self) -> str:
        ...

@dataclass
class BlahUser:
    blah: Blah
    def do_thing_with_blah(self):
        value = self.blah.do_thing()
        return value
