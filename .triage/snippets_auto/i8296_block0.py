"https://github.com/PyCQA/pylint/issues/8296"

date = (2020,1,2,3,4,5)
print("%4d-%02d-%02d %02d:%02d:%02d" % date)

def test_fn(pa_l):
    "my doc"
    return ["Alpha: {alpha:.0%}, Power: {power:.0%}, Nobs={nobs:.1f}".format(**pa)
            for pa in pa_l]
