import re

patterns = {
    'number': r'[0-9]+'
}

# change the types of dictionary values
for name, pattern in patterns.items():
    patterns[name] = re.compile(pattern)

# 1. false positive
for name, pattern in patterns.items():
    print(type(pattern))
    match = pattern.match('testing') # E1101: Instance of 'str' has no 'match' member (no-member)

# 2. works, with warning
for name in patterns: # C0206: Consider iterating with .items() (consider-using-dict-items)
    print(type(patterns[name]))
    match = patterns[name].match('testing')

# 3. false negative
for name in patterns:
    print(type(name))
    match = name.match('testing')
