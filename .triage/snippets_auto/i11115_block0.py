class Container[T: Item]:  # E0601 reported on `Item`
    value: T


class Item:
    pass
