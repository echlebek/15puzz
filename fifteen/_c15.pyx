import numpy as np
cimport numpy as np
from collections import namedtuple


BLANK = 0
SEARCH_LIMIT = 80
SOLVED = np.array(
    [[1, 2, 3, 4],
     [5, 6, 7, 8],
     [9, 10, 11, 12],
     [13, 14, 15, BLANK]],
    dtype=np.uint8
)

class Node(namedtuple("Node", ("distance", "board", "parent"))):
    """
    A `Node` represents a board state which has a `distance` away from
    the starting board state. It has a reference to its `parent` state
    so that the path back to the start can be discovered for any `Node`.
    """
    def __lt__(self, other):
        """
        Necessary so that the numpy array doesn't get compared.
        We don't care about the ordering for equal distances.
        """
        return self.distance < other.distance

    def __repr__(self):
        return repr((self.distance, self.board))

    __slots__ = ()



def search2(queue, set visited):
    """
    `search` iteratively gets `Node`s out of `queue`, adding them to `visited`
    as it goes. For each item, `moves` is called on the node's board. Each
    move is added to the queue if it is not already in the visited set.
    """
    while not queue.empty():
        node = queue.get()

        if all(node.board.flat == SOLVED.flat):
            return node

        visited.add(hash(tuple(node.board.flat)))

        for m in moves2(node.board):
            if node.distance + 1 < SEARCH_LIMIT and hash(tuple(m.flat)) not in visited:
                queue.put(Node(node.distance + 1, m, node))


cpdef list moves2(np.ndarray[np.uint8_t, ndim=2] board):
    """
    `moves` generates the next set of moves for the given board.
    """
    ((i,), (j,)) = np.nonzero(board == BLANK)

    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    newboard = np.copy(board)
    cdef list results = []

    for x, y in moves:
        x += i
        y += j
        try:
            newboard[i, j], newboard[x, y] = newboard[x, y], newboard[i, j]
        except IndexError:
            # Not all moves are valid, for example if the blank is in the
            # corner, only two moves will be valid.
            continue

        results.append(newboard)
        newboard = np.copy(board)

    return results
