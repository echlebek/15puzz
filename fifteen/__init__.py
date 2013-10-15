import numpy as np
from collections import namedtuple
from Queue import PriorityQueue

BLANK = 0
SEARCH_LIMIT = 80  # The shortest path for the 15 puzzle can always be found in 80 movesD

SOLVED = np.array(
    [[1, 2, 3, 4],
     [5, 6, 7, 8],
     [9, 10, 11, 12],
     [13, 14, 15, BLANK]],
    dtype=np.int8
)


import itertools
# pairs for linear conflict
#_pairs = itertools.combinations([0, 1, 2, 3], 2)


class Node(namedtuple("Node", ("distance", "cost", "board", "parent"))):
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
        return (self.distance + self.cost) < (other.distance + other.cost)

    def __repr__(self):
        return repr((self.distance, self.board))

    __slots__ = ()


def moves(board):
    """
    `moves` generates the next set of moves for the given board. It generates
    multi-tile moves, eg, moves where the blank moves one or more spots in a
    given direction.
    """
    ((i,), (j,)) = np.nonzero(board == BLANK)

    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    newboard = np.copy(board)

    for x, y in moves:
        x += i
        y += j
        if x >= 0 and x < 4 and y >= 0 and y < 4:
            # Not all moves are valid, for example if the blank is in the
            # corner, only two moves will be valid.
            newboard[i, j], newboard[x, y] = newboard[x, y], newboard[i, j]

            yield newboard
            newboard = np.copy(board)


def manhattan_distance(board):
    result = 0

    for i in range(4):
        for j in range(4):
            ((x,), (y,)) = np.nonzero(SOLVED == board[i, j])
            result += abs(i - x) + abs(j - y)

    return result


def linear_conflict(board):
    result = 0

    pairs = itertools.combinations([0, 1, 2, 3], 2)
    for row in range(4):
        for j, k in pairs:
            for line in SOLVED:
                if ((board[row, k] < board[row, j])
                    and abs(board[row, k] - board[row, j]) > 3
                    and (board[row, j] != SOLVED[row, j] and board[row, k] != SOLVED[row, k])):

                    result += 2

    return result

def hash_array(array):
    """Gives the hashed result of a numpy array."""
    return hash(tuple(array.flat))


def search(queue, visited):
    """
    `search` iteratively gets `Node`s out of `queue`, adding them to `visited`
    as it goes. For each item, `moves` is called on the node's board. Each
    move is added to the queue if it is not already in the visited set.
    """
    while not queue.empty():
        node = queue.get()

        if all(node.board.flat == SOLVED.flat):
            return node

        visited.add(hash_array(node.board))

        for m in moves(node.board):
            cost = manhattan_distance(m) + linear_conflict(m)
            if node.distance + 1 < SEARCH_LIMIT and hash_array(m) not in visited:
                queue.put(Node(node.distance + 1, cost, m, node))


def _solve(board, searchfun):
    cost = manhattan_distance(board) + linear_conflict(board)
    print cost
    start = Node(0, cost, board, None)
    queue = PriorityQueue()
    queue.put(start)
    visited = set()

    result = searchfun(queue, visited)

    def getpath(node, path):
        path.append(node)
        if node.parent is not None:
            return getpath(node.parent, path)
        else:
            return path

    if queue.empty():
        # Something went wrong with the search algorithm.
        raise ValueError("Bad search")

    return getpath(result, [])


def solve(board):
    """
    This is the top level function of the program. `board` is given to the
    search function by placing it into an empty `PriorityQueue`.

    A path to the result is returned.
    """
    return _solve(board, search)


def solve2(board):
    """Optimized version of solve"""
    from _c15 import search2
    return _solve(board, search2)
