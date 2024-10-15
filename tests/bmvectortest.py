import bmvector.geo2 as bv
import unittest as ut
import numpy as np
from math import sqrt, pi


class Point(ut.TestCase):
    def testinit1(self):
        p = bv.Point(1, 2, 3)
        self.assertEqual(repr(p), "p[1, 2, 3]")

    def testinit2(self):
        a = np.asarray((1, 2, 3))
        p = bv.Point(a)
        self.assertEqual(repr(p), "p[1, 2, 3]")

    def testinit3(self):
        a = [1, 2, 3]
        p = bv.Point(a)
        self.assertEqual(repr(p), "p[1, 2, 3]")

    def testiniterror(self):
        self.assertRaises(ValueError, bv.Point)

    def testadd(self):
        p = bv.Point(0, 0, 0)
        v = bv.Vector(1, 1, 0)
        self.assertTrue(np.all((p + v).val == [1, 1, 0]))
        self.assertTrue(np.all((v + p).val == [1, 1, 0]))
        self.assertTrue(type(p + v) == bv.Point)
        self.assertTrue(type(v + p) == bv.Point)

    def testsub(self):
        p1 = bv.Point(1, 2, 3)
        p2 = bv.Point(0, 1, 2)
        self.assertTrue(type(p1 - p2) == bv.Vector)
        self.assertTrue(np.all((p1 - p2).val == [1, 1, 1]))

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
        v = bv.Vector(1, 1, 1)
        self.assertEqual(v.norm, np.linalg.norm(v.val))

    def testlen(self):
        v = bv.Vector(1, 1, 1)
        self.assertEqual(v.norm, np.linalg.norm(v.val))

    def testnormalized(self):
        v = bv.Vector(1, 1, 1)

        self.assertTrue(
            np.all(v.normalized().val == [1 / sqrt(3), 1 / sqrt(3), 1 / sqrt(3)])
        )

    def testgetdir(self):
        v = bv.Vector(1, 1, 1)
        self.assertEqual(v.getdir(10), v.normalized())

    def testrotate(self):
        v = bv.Vector(1, 1, 1)
        r = bv.Vector(0, 1, 2)
        v2 = bv.Vector((0.44721359549995804, -0.2944271909999159, 1.647213595499958))
        a = -pi / 2
        self.assertLess((v.rotate(r, a).val - v2.val).sum(), 0.0001)


if __name__ == "__main__":
    ut.main()
