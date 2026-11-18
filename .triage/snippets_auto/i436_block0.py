
class KeyedFactoryDefaultDict(collections.defaultdict):
    """Modified defaultdict that passes the key to default_factory calls."""

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        value = self.default_factory(key)
        self[key] = value
        return value

