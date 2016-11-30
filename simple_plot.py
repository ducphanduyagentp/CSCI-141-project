"""
A simple demonstration program to make sure matplotlib is installed
correctly.
"""

import numpy as np
import matplotlib.pyplot as plt
import random
# evenly sampled time at 200ms intervals
t = np.arange(0., 5., 0.2)

# red dashes, blue squares and green triangles

plt.plot(t, t, 'o',label='gg1', color=tuple([random.random() for _ in range(3)]))
plt.plot(t, t**2, 'o', label='gg2', color=tuple([random.random() for _ in range(3)]))
plt.plot(t, t**3, 'o', label='gg3', color=tuple([random.random() for _ in range(3)]), linestyle='-')
plt.plot(t, t**4, 'o', label='gg4', color=(1,1,1), linestyle='-')
plt.legend(loc='best')
plt.show()
