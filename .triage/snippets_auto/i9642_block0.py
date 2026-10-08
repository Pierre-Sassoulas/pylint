"""doc"""

def f():
    """doc"""

    for i in []:
        if i:
            fail1 = 42
    print(fail1)  # bug detected

    for i in []:
        fail2 = 42
    print(fail2)  # bug not detected

