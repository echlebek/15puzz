import numpy as np
from collections import namedtuple
from Queue import PriorityQueue

BLANK = 0
SEARCH_LIMIT = 80  # The shortest path for the 15 puzzle can always be found in 80 moves

SOLVED = np.array(
    [[1, 2, 3, 4],
     [5, 6, 7, 8],
     [9, 10, 11, 12],
     [13, 14, 15, BLANK]],
    dtype=np.uint8
)


class Node(namedtuple("Node", ("distance", "board", "parent"))):
    def __lt__(self, other):
        """
        Necessary so that the numpy array doesn't get compared.
        We don't care about the ordering for equal distances.
        """
        return self.distance < other.distance

    def __repr__(self):
        return repr((self.distance, self.board))

    __slots__ = ()


def moves(board):
    ((i,), (j,)) = np.nonzero(board == BLANK)

    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    newboard = np.copy(board)

    for x, y in moves:
        x += i
        y += j
        try:
            newboard[i, j], newboard[x, y] = newboard[x, y], newboard[i, j]
        except IndexError:
            continue

        yield newboard
        newboard = np.copy(board)


def hash_array(array):
    return tuple(array.flat)


def search(queue, visited):
    while True:
        node = queue.get()

        if all(node.board.flat == SOLVED.flat):
            return node

        visited.add(hash_array(node.board))

        for m in moves(node.board):
            if node.distance + 1 < SEARCH_LIMIT and hash_array(m) not in visited:
                queue.put(Node(node.distance + 1, m, node))


def solve(board):
    start = Node(0, board, None)
    queue = PriorityQueue()
    queue.put(start)
    visited = set()

    result = search(queue, visited)

    def getpath(node, path):
        path.append(node)
        if node.parent is not None:
            return getpath(node.parent, path)
        else:
            return path

    return getpath(result, [])
