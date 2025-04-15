import numpy as np
import numpy.linalg as la
from math import acos, sin, tan, pi, sqrt, cos
from pyquaternion import Quaternion
import matplotlib.pyplot as plt
from numpy import ndarray


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
    r2 = la.norm(v1) * tan(a / 2) * 0.9
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


def fillet7d(v1: ndarray, v2: ndarray, p: float, maxa: float):
    """Fillets two 7d vectors with a 3d arc.
    Calculates speed on arc as min v1, v2 speeds, limited with centripetal acceleration.
    ABC vector sum is preserved. Extrusion amnt is reduced in proportion to path length.

    Args:
        v1 (ndarray): Input vector of format [XYZABCEF]
        v2 (ndarray): Output vector of format [XYZABCEF]
        p (float): Distance from corner to arc (precision) in 3d space
        maxa (float): Centripetal acceleration to calc max speed on arc

    Returns:
        tuple:
            v1t7 (ndarray): Trimed input vector of format [XYZABCEF]
            (ad, ch7):
                ad (ndarray): Arc start direction [XYZ]. Is normalized.
                ch7 (ndarray): Arc chord vector of format [XYZABCEF]
            v2t7 (ndarray): Trimed output vector of format [XYZABCEF]

    rmk: If vectors are colinear or inverted returns input vectors
    """

    if abs(np.dot(v1[:3], v2[:3]) / la.norm(v1[:3]) / la.norm(v2[:3])) == 1:
        return v1, v2
    else:
        if p <= 0:
            raise ValueError(f"Precision must be >0, {p} given")
        if maxa <= 0:
            raise ValueError(f"Max acc must be >0, {maxa} given")

        v1t, ch, v2t = fillet(v1[:3], v2[:3], p)  # FOL Let's calc 3d fillet arc
        r, l = arcparam(v1t, ch)  # Then it's radius and length
        v1t7 = (
            v1 / la.norm(v1[:3]) * la.norm(v1t)
        )  # Trim vectors in proportion to its 3d repr
        v2t7 = v2 / la.norm(v2[:3]) * la.norm(v2t)
        v1t7[7] = v1[7]  # But preserve speed
        v2t7[7] = v2[7]
        ch7 = np.zeros(8, float)
        ch7[:3] = ch[:3]  # First 3d of arc chord are as for 3d arc
        ch7[3:6] = (
            v1[3:6] + v2[3:6] - v1t7[3:6] - v2t7[3:6]
        )  # Calc ABC of 7d arc to preserve total path
        t1 = la.norm(v1[:3]) - la.norm(v1t7[:3])  # Trimmed length of first vector
        e1 = v1[6] - v1t7[6]  # Trimmed extrision amnt of first vector
        t2 = la.norm(v2[:3]) - la.norm(v2t7[:3])  # The same for second vector
        e2 = v2[6] / la.norm(v2[:3]) * t2
        ch7[6] = (
            (e1 + e2) / (t1 + t2) * l
        )  # Calc arc extrusion amnt preserving med speed
        maxv = sqrt(maxa * r)  # Calc max arc vel from max acc and it's radius
        ch7[7] = min(maxv, v1[7], v2[7])  # Set arc vel
        ad = v1[:3] / la.norm(v1[:3])  # Calc arc start dir 3d vector
        return v1t7, (ad, ch7), v2t7


if __name__ == "__main__":
    pass
    # np.set_printoptions(precision=2, suppress=True)
    # v1 = np.array((2, 0, 0, 5, 6, 7, 50, 100))
    # v2 = np.array((0, 100, 0, 8, 9, 12, 30, 150))
    # v1t, (ad, av), v2t = fillet7d(v1, v2, 1, 1000)

    # print(v1t, (ad, av), v2t, sep="\n")
    # print(*arcparam(ad, av[:3]))
    # print(v1 + v2, v1t + av + v2t)

    # p1 = [[0, 0, 0]]
    # for v in (v1, v2):
    #     p1.append(p1[-1] + v)

    # p2 = [[0, 0, 0]]
    # p2.append(p2[0] + v1t)
    # for p in arcinterp(v1t, rv):
    #     p2.append(p2[-1] + p)
    # p2.append(p2[-1] + v2t)
    # # plt.plot(*zip(*p1), "r")
    # # plt.plot(*zip(*p2), "g")
    # ax = plt.figure().add_subplot(projection="3d")
    # ax.plot(*zip(*p1), "r")
    # ax.plot(*zip(*p2), "g")
    # plt.axis("equal")
    # plt.show()
    # v1 = np.array((10, 0, -10), float)
    # v2 = np.array((0, -10, 10), float)
    # a = fillet(v1, v2, 3)
    # print(a[:2])
    # print(arcparam(a[0], a[1]))
