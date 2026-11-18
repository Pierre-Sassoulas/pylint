#!python

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    str_dict = enums.copy()
    enums['reverse'] = dict((value, key) for key, value in enums.items())
    enums['str_dict'] = str_dict

    return type('Enum', (), enums)

RESULT_SEVERITY = enum("INFO", "NORMAL", "MAJOR")
RESULT_SEVERITY.__str__ = lambda x: RESULT_SEVERITY.reverse.get(x, "NORMAL")

print(RESULT_SEVERITY.INFO)

