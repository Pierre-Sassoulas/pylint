import operator

a = [1, 2, 3]
key = operator.itemgetter(0)
print(a[key([4, 5, 6])])
