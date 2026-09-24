class A:
    def __init__(self, b=False):
        self._m = [] if b else None

    def reset(self):
        if self._m:
            del self._m[:]
