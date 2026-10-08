### file "mwe/__init__.py"
# empty


### file "mwe/sub_item.py"

class SubItem:
    def __init__(self, name: str = "abc") -> None:
        self.real_name: str = name


### file "mwe/item.py"

from mwe.sub_item import SubItem

class Item:
    def __init__(self) -> None:
        self.sub_item: SubItem = SubItem()

    def set_name(self, name: str) -> None:
        self.sub_item.name = name
