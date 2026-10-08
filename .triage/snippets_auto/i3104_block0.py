import numpy as np
from scipy.spatial import cKDTree
x, y = np.mgrid[0:5, 2:8]
tree = cKDTree(np.c_[x.ravel(), y.ravel()])

dd, ii = tree.query([[0, 0], [2.1, 2.9]], k=1)
print(dd, ii)

print(tree.data[ii]) 
