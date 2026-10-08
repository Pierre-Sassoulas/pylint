class _Singleton:
    instance: '_Singleton' = None

    def __contains__(self, item):
        return item in ["a"]


# pylint: disable=invalid-name
def Singleton() -> _Singleton:
    """Returns instance of Singleton"""
    if _Singleton.instance is None:
        _Singleton.instance = _Singleton()
    return _Singleton.instance

print("a" in Singleton())
print("b" in Singleton())
