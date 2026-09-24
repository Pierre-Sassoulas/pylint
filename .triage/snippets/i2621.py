def _fn_a():
    return _fn_b() + (3,)


def _fn_c():
    vp1 = 1
    if vp1 < 0:
        vp1 = -vp1
    return vp1


def _fn_b():
    vp1 = _fn_c()
    return 1, vp1


A1, B1, C1 = _fn_a()
