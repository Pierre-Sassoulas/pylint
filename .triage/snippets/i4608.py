import random

if random.choice([0, 1]):
    x = None
else:
    x = 15

y = -x if x is not None else None
