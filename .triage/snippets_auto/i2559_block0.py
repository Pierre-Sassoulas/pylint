class MyApp(metaclass=abc.ABCMeta):
    ...
    def lock_name(self):
        "Lock file name, mutex apps should redefine this to return a string."
        return None

    def lock_path(self):
        "Lock file path, based on lock_name()."
        lock_path = self.lock_name()
        if lock_path is None:
            return None
        ...
