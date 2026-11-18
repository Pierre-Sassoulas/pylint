#pylint:disable=missing-docstring
#pylint:enable=nested-min-max

def bounds(lo, hi, elements):
    return (
        min(lo, hi, min(elements)),
        max(lo, hi, max(elements)),
    )
