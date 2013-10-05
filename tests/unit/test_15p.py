import unittest
import numpy as np


class Test15Puzzle(unittest.TestCase):

    def test_moves(self):
        from fifteen import moves, SOLVED, BLANK

        m = moves(SOLVED)

        b = next(m)
        e = np.array([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, BLANK, 15]
        ], dtype=np.uint8)
        np.testing.assert_array_equal(b, e)

        b = next(m)
        e = np.array([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, BLANK],
            [13, 14, 15, 12]
        ], dtype=np.uint8)

        np.testing.assert_array_equal(b, e)

        with self.assertRaises(StopIteration):
            next(m)


if __name__ == "__main__":
    unittest.main()
