from enum import Flag


class MosaicFlags(Flag):
    NONE = 0
    SUPPLY_MUTABLE = 1
    TRANSFERABLE = 2
    RESTRICTABLE = 4
    REVOKABLE = 8


value = MosaicFlags.SUPPLY_MUTABLE | MosaicFlags.RESTRICTABLE | MosaicFlags.REVOKABLE
print(value)
