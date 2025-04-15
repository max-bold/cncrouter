import numpy as np
import numpy.linalg as la
from math import acos, sin, tan, pi, sqrt, cos
from pyquaternion import Quaternion
import matplotlib.pyplot as plt


def fillet(v1, v2, p):
    """Creates a fillet between two vectors with given distance from corner to the arc.
    Returns two trimed vectors and arc vector (chord). Arc direction is always eq to v1.
    Trimed vectors

    Args:
        v1 (_type_): _description_
        v2 (_type_): _description_
        p (_type_): _description_

    Returns:
        _type_: _description_
    """    
    a = pi - acos(np.dot(v1, v2) / la.norm(v1) / la.norm(v2))
    s = sin(a / 2)
    r1 = p * s / (1 - s)
    r2 = la.norm(v1) * tan(a / 2) / 2
    r3 = la.norm(v2) * tan(a / 2) / 2
    r = min(r1, r2, r3)
    t = r / tan(a / 2)
    v1t = v1 / la.norm(v1) * (la.norm(v1) - t)
    v2t = v2 / la.norm(v2) * (la.norm(v2) - t)
    n = np.cross(v1, v2)
    q = Quaternion(axis=n, angle=(pi - a) / 2)
    c = t * sin(a / 2) * 2
    cv = v1 / la.norm(v1) * c
    rv = q.rotate(cv)
    return v1t, rv, v2t


def arcinterp(v1, v2):
    b = acos(np.dot(v1, v2) / la.norm(v1) / la.norm(v2))
    a = pi - b * 2
    r = la.norm(v2) / 2 / cos(a / 2)
    n = np.cross(v1, v2)
    c = v1 / la.norm(v1) * r
    q1 = Quaternion(axis=n, angle=pi / 2)
    c = q1.rotate(c)
    c3 = c
    res = []
    for i in np.linspace(0, 2 * b, 20):
        q2 = Quaternion(axis=n, angle=i)
        c2 = q2.rotate(-c)
        res.append(c3 + c2)
        c3 = -c2
    return res


def arcparam(v1, v2):
    b = acos(np.dot(v1, v2) / la.norm(v1) / la.norm(v2))
    r = la.norm(v2) / 2 / sin(b)
    l = r * 2 * b
    return r, l


if __name__ == "__main__":
    v1 = np.array((-10, 0, 0))
    v2 = np.array((-10, -.1, 0))
    v1t, rv, v2t = fillet(v1, v2, 3)
    print(v1t, rv, v2t)
    print(*arcparam(v1t,rv))
    p1 = [[0, 0]]
    p1.append(p1[0] + v1[:2])
    p1.append(p1[1] + v2[:2])

    p2 = [[0, 0]]
    p2.append(p2[0] + v1t[:2])
    for p in arcinterp(v1t, rv):
        p2.append(p2[-1] + p[:2])
    # p2.append(p2[1] + rv[:2])
    p2.append(p2[-1] + v2t[:2])
    plt.plot(*zip(*p1), "r")
    plt.plot(*zip(*p2), "g")
    plt.axis("equal")
    plt.show()

    # v1=np.array((10,10,0))
    # v2=np.array((10,-10,0))
    # r = arcinterp(v1,v2)
    # plt.plot(*zip(*r))
    # plt.axis("equal")
    # plt.show()
