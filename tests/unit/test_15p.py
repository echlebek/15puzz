import unittest
import numpy as np
from fifteen import SOLVED, BLANK, Node
from fifteen.search import search, solve
from Queue import PriorityQueue
from _c15 import moves


class Test15Puzzle(unittest.TestCase):

    def test_moves(self):

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

    def test_search(self):
        board = np.array(
            [[1, 2, 3, 4],
             [5, 6, 7, 8],
             [9, 10, 11, 12],
             [13, BLANK, 14, 15]],
        dtype=np.uint8)

        queue = PriorityQueue()
        queue.put(Node(0, board, None))
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

    def test_solve(self):
        board = np.array([[5, 1, 2, 4],
                          [9, 6, 3, 8],
                          [10, 14, 7, 11],
                          [13, BLANK, 15, 12]],
                         dtype=np.uint8)

        self.assertEquals(len(solve(board)), 11)


if __name__ == "__main__":
    unittest.main()
