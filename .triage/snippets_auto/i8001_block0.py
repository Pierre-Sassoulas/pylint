# first line is line number 36
def create_link(osm: OsmObject, wd: WdItem, key: str) -> Link:
    if isinstance(osm, OsmNode):
        return NodeLink(osm, wd, key) # line 38
    if isinstance(osm, OsmWay):
        return WayLink(osm, wd, key) # line 40
    if isinstance(osm, OsmRelation):
        return RelationLink(osm, wd, key) # line 42
    if isinstance(osm, OsmArea):
        return AreaLink(osm, wd, key) # line 44
    raise TypeError()
