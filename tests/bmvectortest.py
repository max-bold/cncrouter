import bmvector.geo2 as bv
import unittest as ut
import numpy as np
from math import sqrt, pi


class Point(ut.TestCase):
    def testinit1(self):
        p = bv.Point(1, 2, 3)
        self.assertTrue(np.all(p.val == [1, 2, 3, 0, 0, 0, 0]))

    def testinit2(self):
        a = np.asarray((1, 2, 3))
        p = bv.Point(a)
        self.assertTrue(np.all(p.val == [1, 2, 3, 0, 0, 0, 0]))

    def testinit3(self):
        a = [1, 2, 3]
        p = bv.Point(a)
        self.assertTrue(np.all(p.val == [1, 2, 3, 0, 0, 0, 0]))

    def testiniterror(self):
        self.assertRaises(ValueError, bv.Point)

    def testadd(self):
        p = bv.Point(0, 0, 0)
        v = bv.Vector(1, 1, 0)
        self.assertTrue(np.all((p + v).val == [1, 1, 0, 0, 0, 0, 0]))
        self.assertTrue(np.all((v + p).val == [1, 1, 0, 0, 0, 0, 0]))
        self.assertTrue(type(p + v) == bv.Point)
        self.assertTrue(type(v + p) == bv.Point)

    def testsub(self):
        p1 = bv.Point(1, 2, 3)
        p2 = bv.Point(0, 1, 2)
        self.assertTrue(type(p1 - p2) == bv.Vector)
        self.assertTrue(np.all((p1 - p2).val == [1, 1, 1, 0, 0, 0, 0]))

    def testeq(self):
        p1 = bv.Point(1, 2, 3)
        p2 = bv.Point(0, 1, 2)
        p3 = bv.Point(1, 2, 3)
        v = bv.Vector(1, 2, 3)
        self.assertTrue(p1 == p3)
        self.assertFalse(p1 == p2)
        self.assertFalse(p1 == v)
        self.assertFalse(v == p1)


class Vector(ut.TestCase):
    def testnorm(self):
        v = bv.Vector(1, 1, 1, 1)
        self.assertEqual(v.norm, np.linalg.norm(v.val))

    def testlen(self):
        v = bv.Vector(1, 1, 1, 23)
        self.assertEqual(v.len, np.linalg.norm(v.val[:3]))

    def testnormalized(self):
        v = bv.Vector(1, 1, 1, 1)
        nv = bv.Vector(0.5, 0.5, 0.5, 0.5)

        # self.assertTrue(np.all(v.normalized().val == [0.5, 0.5, 0.5, 0.5, 0, 0, 0]))
        self.assertEqual(v.normalized(), nv)

    def testgetdir(self):
        v = bv.Vector(1, 1, 1, 23)
        rv = bv.Vector(1 / sqrt(3), 1 / sqrt(3), 1 / sqrt(3))
        self.assertEqual(v.getdir(10), rv)
        self.assertEqual(v.getdir(), rv)

    def testrotate(self):
        v = bv.Vector(1, 1, 1, 4)
        ra = bv.Vector(0, 1, 2)
        ran = ra.normalized()
        rv = bv.Vector(0.44721359549995804, -0.2944271909999159, 1.647213595499958, 4)
        a = -pi / 2
        # self.assertLess((v.rotate(ra, a).val - rv.val).sum(), 0.0001)
        self.assertEqual(v.rotate(ra, a), rv)
        self.assertEqual(v.rotate(ran, a), rv)

    def testcross(self):
        x = bv.Vector(1, 0, 0, 23)
        y = bv.Vector(0, 1, 0, 25)
        z = bv.Vector(0, 0, 1)
        self.assertEqual(x.cross(y), z)
        self.assertEqual(bv.Vector.cross(x, y), z)

    def testangleto(self):
        a = bv.Vector(1, 0)
        b = bv.Vector(1, 1)
        self.assertAlmostEqual(a.angleto(b), pi / 4)
        self.assertAlmostEqual(bv.Vector.angleto(a, b), pi / 4)


if __name__ == "__main__":
    ut.main()
