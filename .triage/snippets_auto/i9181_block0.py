import dataclasses
from typing import Any, cast


@dataclasses.dataclass(kw_only=True)
class Resource:
    name: str


@dataclasses.dataclass(kw_only=True)
class ResourceParent:
    resource: Resource

    def __post_init__(self) -> None:
        if isinstance(self.resource, dict):
            self.resource = Resource(**cast(dict[str, Any], self.resource))
