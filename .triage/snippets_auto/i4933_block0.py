class Hashable:
    pass


class NotHashable:
    def __eq__(self, other):
        return self == other


class HashableAgain:
    def __eq__(self, other):
        return self == other

    def __hash__(self):
        return id(self)

x in (1, Hashable, HashableAgain)  # [use-set-for-membership]
x in (1, NotHashable)  # List is not hashable
