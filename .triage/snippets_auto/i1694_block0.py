class classproperty(classmethod):

    def __init__(self, fget):
        if isinstance(fget, (classmethod, staticmethod)):
            self.fget = lambda cls: fget.__get__(None, cls)()
        else:
            self.fget = fget
        self.cached = {}
        super(classproperty, self).__init__(self.fget)

    def __get__(self, instance, cls):
        if cls in self.cached:
            return self.cached[cls]
        value = self.cached[cls] = self.fget(cls)
        return value

