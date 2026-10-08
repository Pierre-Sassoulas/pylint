# test.py

FRUITS = {"apple": 1, "orange": 10, "berry": 22}


def pick_fruit(name):
    for fruit_name, count in FRUITS.items():
        if fruit_name == name:
            print(FRUITS[name])  # should be  [unnecessary-dict-index-lookup]
