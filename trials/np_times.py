import numpy as np


class times(np.ndarray):
    def __new__(cls):
        return np.zeros(7, float).view(cls)

    def __setitem__(self, key, value):
        value = max(value, 0)
        if key == 0 or key == 2:
            super().__setitem__(0, value)
            super().__setitem__(2, value)
        elif key == 4 or key == 6:
            super().__setitem__(4, value)
            super().__setitem__(6, value)
        else:
            super().__setitem__(key, value)


ts = times()
print(ts)
ts[0] += 12
print(ts)
ts[6] -= 2
ts-=3
print(ts)
