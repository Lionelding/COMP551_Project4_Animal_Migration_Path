from __future__ import print_function
import numpy as np
from dtw import dtw

x = np.array([1,1,1,1,4,4,4,4,1,1,1,1,4,4,4,4,1,1,1,1,4,4,4,4])
y = np.array([4,4,4,4,1,1,1,1,4,4,4,4,1,1,1,1,4,4,4,4,1,1,1,1])

dist, _, _ = dtw(x,y)

print('dist')
print(dist)

dist, _, _ = dtw(x, y, w=1)

print('dist')
print(dist)
