import unittest
import numpy as np
from fifteen import moves, SOLVED, BLANK, search, Node
from Queue import PriorityQueue


class Test15Puzzle(unittest.TestCase):

    def test_moves(self):

        m = moves(SOLVED)

        b = next(m)
        e = np.array([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, BLANK, 15]
        ], dtype=np.int8)
        np.testing.assert_array_equal(b, e)

        b = next(m)
        e = np.array([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, BLANK],
            [13, 14, 15, 12]
        ], dtype=np.int8)

        np.testing.assert_array_equal(b, e)

        with self.assertRaises(StopIteration):
            next(m)

    def test_search(self):
        board = np.array(
            [[1, 2, 3, 4],
             [5, 6, 7, 8],
             [9, 10, 11, 12],
             [13, BLANK, 14, 15]],
        dtype=np.int8)

        queue = PriorityQueue()
        queue.put(Node(0, 0, board, None))
        solution = search(queue, set())
        path = []
        node = solution
        while True:
            path.append(node)
            if node.parent is not None:
                node = node.parent
            else:
                break

        self.assertEquals(len(path), 3)

    def _solve(self, solvefun):

        board = np.array([[5, 1, 2, 4],
                          [9, 6, 3, 8],
                          [10, 14, 7, 11],
                          [13, BLANK, 15, 12]],
                         dtype=np.int8)

        self.assertEquals(len(solvefun(board)), 11)

    def test_solve(self):
        from fifteen import solve

        self._solve(solve)

    def test_solve2(self):
        from fifteen import solve2
        self._solve(solve2)


if __name__ == "__main__":
    unittest.main()
