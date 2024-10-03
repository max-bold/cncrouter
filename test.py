import unittest
import geo


class GeoTest(unittest.TestCase):

    def testpvsum(self):
        p = geo.Point(5, 7)
        v = geo.Vecor(2, 3)
        self.assertEqual(v + p, geo.Point(7, 10))

    def testlen(self):
        v = geo.Vecor(3, 3)
        self.assertEqual(v.len, (3**2 + 3**2) ** 0.5)


if __name__ == "__main__":
    unittest.main()
