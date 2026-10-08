@dataclass
class Link(ABC):
    osm: OsmObject
    wd: WdItem
    key: str

@dataclass
class NodeLink(Link):
    osm: OsmNode

# ... same for the others
