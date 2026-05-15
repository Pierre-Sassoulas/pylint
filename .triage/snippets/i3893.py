class PV1Axis:
    def __init__(
        self, polygon, capacity, filename, column, build_limit=None, label="PV"
    ):
        pass


class Wind:
    def __init__(
        self,
        polygon,
        capacity,
        filename,
        column,
        delimiter=None,
        build_limit=None,
        label="wind",
    ):
        pass


for g in [PV1Axis, Wind]:
    if g == Wind:
        g(0, 0, "foo", 0, delimiter=",", build_limit=100, label="wind")
