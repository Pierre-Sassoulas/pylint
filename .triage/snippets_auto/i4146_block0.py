import time
from timeit import timeit


def not_all(n, step=1):
    if not all(range(-n, n, step)):
        ...


def any_not(n, step=1):
    if any(x for x in range(-n, n, step)):
        ...


assert not_all(3, 1) == any_not(3, 1)
assert not_all(3, 2) == any_not(3, 2)
assert not_all(5, 1) == any_not(5, 1)

start = time.time()
for i in range(20):
    any_not(1000000)
end = time.time()
print(end - start)
start = time.time()
for i in range(20):
    not_all(1000000)
end = time.time()
print(end - start)

print(
    timeit(
        "import numpy as np; arr = np.ones(int(1e8)); arr[3]=0; np.any(arr<=0)",
        number=10,
    )
)
print(
    timeit(
        "import numpy as np; arr = np.ones(int(1e8)); arr[3]=0; np.all(arr>0)",
        number=10,
    )
)

