class NamedObject:
    def __init__(self, names):
        self._org_names = names
        self._names = None

    def _determine_names(self):
        self._names = [n.lower() for n in self._org_names]

    @property
    def names(self):
        if self._names is None:
            self._determine_names()
        return self._names


obj1 = NamedObject(["Bla"])
names1 = obj1.names
names1_u = [n.upper() for n in names1]
print(names1_u)
