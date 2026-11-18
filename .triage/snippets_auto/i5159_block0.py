from dataclasses import dataclass, field

@dataclass
class Expandable:
    _api: field()
    var = []
