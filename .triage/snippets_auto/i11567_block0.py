`arguments-differ` (W0221) raises a false positive when using positional-only parameters.


# repro.py
class Base:
    def method(self, key):
        return key

class Child(Base):
    def method(self, key, /):
        return key
