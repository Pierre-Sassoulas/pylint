test.py:

from collections.abc import MutableMapping
from typing import cast
import pygtrie

T = MutableMapping[str, dict[str, int]]

if __name__ == '__main__':
    x: T = pygtrie.CharTrie({'a': {'b': 'c'}})
    y: pygtrie.CharTrie[str, dict[str, int]] = pygtrie.CharTrie({'a': {'b': 'c'}})
    z: dict[str, dict[str, int]] = {'a': {'b': 'c'}}

    # x and y print() lines trigger unsubscriptable-object, but z does not:
    print(x['a']['b'])
    print(cast(dict[str, dict[str, int]], x['a'])['b'])
    print(cast(pygtrie.CharTrie[str, dict[str, int]], x['a'])['b'])
    print(y['a']['b'])
    print(cast(T, y['a'])['b'])
    print(cast(dict[str, dict[str, int]], y['a'])['b'])
    print(z['a']['b'])
    print(cast(T, z['a'])['b'])
    print(cast(pygtrie.CharTrie[str, dict[str, int]], z['a'])['b'])
