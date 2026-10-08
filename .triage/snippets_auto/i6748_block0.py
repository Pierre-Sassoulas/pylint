from dataclasses import dataclass
import collections


@dataclass
class Shadow:

    collections: collections.deque
    other: collections.defaultdict


print(Shadow(collections.deque(), collections.defaultdict()))
