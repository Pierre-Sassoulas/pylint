"""Incorrect Code"""
mylist = list((1, 2, 3, 4, 5))  # [use-list-literal]
mytuple = tuple()  # [use-tuple-literal]
mytuple2 = tuple(['foo', 'bar'])  # [use-tuple-literal]
mydict = dict((('a', 1), ('b', 2)))  # [use-dict-literal]
myset = set(['py', 'lint'])  # [use-set-literal]
