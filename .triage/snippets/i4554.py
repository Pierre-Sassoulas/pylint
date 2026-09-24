import os.path


def bad():
    a = []
    a.extend(["a", "b"])
    return os.path.join(*a)
