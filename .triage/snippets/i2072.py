a = None
for i in range(1, 5):
    if i % 2:
        a = "foo"
    elif not i % 2:
        a = a[1:]
