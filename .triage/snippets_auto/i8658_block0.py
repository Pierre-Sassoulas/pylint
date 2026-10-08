import random

enter_first = True
while enter_first or (some_walrus := random.random()) < 0.9:
    print(some_walrus)
    enter_first = False
