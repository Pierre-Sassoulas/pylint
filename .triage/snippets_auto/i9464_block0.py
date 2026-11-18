import random
from typing import Optional

var: Optional[int] = None

def maybe_modify() -> None:
    global var
    if random.randint(0, 1) == 0:
        var = 1

def test1() -> None:
    global var
    maybe_modify()
    if var is None:
        return
    print(-var)

def test2() -> None:
    global var
    maybe_modify()
    if var is None:
        pass
    else:
        print(-var)

def main():
    test2() # pylint correctly has no issues with test2
    test1() # but has a problem with test1

if __name__ == '__main__':
    main()
