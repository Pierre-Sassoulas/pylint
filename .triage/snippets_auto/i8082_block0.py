class Foo:
    root_dir = "/default_path/"  # not to be specified in __init__

    def __init__(self, file):
        self.path = self.root_dir + file

    @classmethod
    def from_alt_path(cls, alternative_dir, *args, **kwargs):
        obj = super().__new__(cls)
        obj.root_dir = alternative_dir
        obj.__init__(*args, **kwargs)  # ✘ unnecessary-dunder-call
        return obj
