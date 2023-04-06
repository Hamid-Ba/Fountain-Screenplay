import numpy as np

the_arr = np.array([1, 2])

np.save()
with open("test.npy", "wb") as f:
    np.save(f, np.array([1, 2]))
    np.save(f, np.array([1, 3]))
