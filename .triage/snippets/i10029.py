def fun(a, b, *, c, d, **kwargs):
    return a + b + c + d + kwargs["e"] + kwargs["f"]


someargs = {}
someargs["c"] = 3
someargs["d"] = 4
someargs["e"] = 5
someargs["f"] = 6
someargs["g"] = 7

rval = fun(1, 2, **someargs)
print(rval)
