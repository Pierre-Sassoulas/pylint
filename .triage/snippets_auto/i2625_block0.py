"""Shapely no-member false positive MCVE"""
from shapely import wkt
from shapely.geometry import Polygon

POLYGON = Polygon([(0, 0), (0, 1), (1, 1)])
print(POLYGON.exterior.wkt)
print(POLYGON.convex_hull.exterior.wkt)

POLYGON = wkt.loads(POLYGON.wkt)
print(POLYGON.exterior.wkt)
