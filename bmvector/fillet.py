import numpy as np
import numpy.linalg as la
from math import acos, sin, tan, pi, sqrt, cos
from pyquaternion import Quaternion
import matplotlib.pyplot as plt


def fillet(v1, v2, p):
    """Creates a fillet between two vectors with given distance from corner to the arc.
    Returns two trimed vectors and arc vector (chord). Arc direction is always eq to v1.
    Vectors are trimed not more:
        input vector to 0.1 of length
        output vector to 0.5 of length

    Args:
        v1 (ndarray[3,float]): input vector
        v2 (ndarray[3,float]): output vector
        p (float): max distance from corner to arc

    Returns:
        tupple: 
            v1t (ndarray[3,float]): trimed input vector, 
            rv (ndarray[3,float]): arc chord vector, 
            v2t (ndarray[3,float]): trimed output vector
    """    
    a = pi - acos(np.dot(v1, v2) / la.norm(v1) / la.norm(v2))
    s = sin(a / 2)
    r1 = p * s / (1 - s)
    r2 = la.norm(v1) * tan(a / 2)*0.9
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


def arcinterp(v1, v2, k=20):
    """interpolates arc given with input dir and chord vector

    Args:
        v1 (ndarray[3,float]): input dir vector (of any length)
        v2 (ndarray[3,float]): chord vector
        k (int, optional): Number of steps. Defaults to 20.

    Returns:
        list[ndarray[3,float]]: list of vectors representing the arc
    """    
    b = acos(np.dot(v1, v2) / la.norm(v1) / la.norm(v2))
    a = pi - b * 2
    r = la.norm(v2) / 2 / cos(a / 2)
    n = np.cross(v1, v2)
    c = v1 / la.norm(v1) * r
    q1 = Quaternion(axis=n, angle=pi / 2)
    c = q1.rotate(c)
    c3 = c
    res = []
    for i in np.linspace(0, 2 * b, k):
        q2 = Quaternion(axis=n, angle=i)
        c2 = q2.rotate(-c)
        res.append(c3 + c2)
        c3 = -c2
    return res


def arcparam(v1, v2):
    """Returns arc length and radius

    Args:
        v1 (ndarray[3,float]): input dir
        v2 (ndarray[3,float]): chord vector

    Returns:
        tupple(float): 
            r: radius
            l: length
    """    
    b = acos(np.dot(v1, v2) / la.norm(v1) / la.norm(v2))
    r = la.norm(v2) / 2 / sin(b)
    l = r * 2 * b
    return r, l


if __name__ == "__main__":
    v1 = np.array((-10, 0, 0))
    v2 = np.array((-10, -.1, 0))
    v1t, rv, v2t = fillet(v1, v2, 0.1)
    print(v1t, rv, v2t)
    print(*arcparam(v1t,rv))
    p1 = [[0, 0]]
    p1.append(p1[0] + v1[:2])
    p1.append(p1[1] + v2[:2])

    p2 = [[0, 0]]
    p2.append(p2[0] + v1t[:2])
    for p in arcinterp(v1t, rv):
        p2.append(p2[-1] + p[:2])
    p2.append(p2[-1] + v2t[:2])
    plt.plot(*zip(*p1), "r")
    plt.plot(*zip(*p2), "g")
    plt.axis("equal")
    plt.show()
