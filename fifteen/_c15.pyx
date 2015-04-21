# cython: profile=True
import numpy as np
cimport numpy as np
from collections import namedtuple
import itertools
cimport cython


cdef np.int8_t BLANK = 0
cdef int SEARCH_LIMIT = 80
SOLVED = np.array(
    [[1, 2, 3, 4],
     [5, 6, 7, 8],
     [9, 10, 11, 12],
     [13, 14, 15, BLANK]],
    dtype=np.int8
)

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


cdef int manhattan_distance(np.ndarray[np.int8_t, ndim=2] board):
    """Manhattan distance finds how many squares out of place each value in
    `board` is. This is also known as "taxicab distance".
    """
    cdef int result = 0
    cdef int i, j, x, y
    cdef int* find_result = [0, 0]  # Store the indices of the find() result in here

    for i in range(4):
        for j in range(4):
            find(SOLVED, board[i, j], find_result)
            x = find_result[0]
            y = find_result[1]
            result += abs(i - x) + abs(j - y)

    return result


@cython.profile(False)
cdef inline void find(np.ndarray[np.int8_t, ndim=2] board, np.int8_t value, int *result):
    """`find` finds the indices of `value` in `board` and stores them in `result`."""
    cdef int i, j
    for i in range(4):
        for j in range(4):
            if board[i, j] == value:
                # find will always find the value; the caller's risk to take.
                result[0] = i
                result[1] = j
                return


cpdef search2(queue, set visited):
    """
    `search` iteratively gets `Node`s out of `queue`, adding them to `visited`
    as it goes. For each item, `moves` is called on the node's board. Each
    move is added to the queue if it is not already in the visited set.
    """
    cdef int i, j, cost
    cdef int iter = 0
    while not queue.empty():
        node = queue.get()

        if solved(node.board):
            return node

        # node.board.flags.writeable = False
        visited.add(str(node.board.data))

        for m in moves2(node.board):
            cost = manhattan_distance(m)
            # m.flags.writeable = False
            if str(m.data) not in visited:
                queue.put(Node(node.distance + 1, cost, m, node))


cdef bint solved(np.ndarray[np.int8_t, ndim=2] board):
    """`solved` checks to see if the board in question is the solution."""
    cdef int i, j
    for i in range(4):
        for j in range(4):
            if board[i, j] != SOLVED[i, j]:
                return False
    return True


cdef list moves2(np.ndarray[np.int8_t, ndim=2] board):
    """
    `moves` generates the next set of moves for the given board.
    """
    cdef int i, j, x, y

    cdef int* find_result = [0, 0]
    find(board, BLANK, find_result)
    i = find_result[0]
    j = find_result[1]

    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    newboard = np.copy(board)
    cdef list results = []

    for m in range(4):
        x = moves[m][0] + i
        y = moves[m][1] + j
        if x >= 0 and x < 4 and y >= 0 and y < 4:
            # Not all moves are valid, for example if the blank is in the
            # corner, only two moves will be valid.
            newboard[i, j], newboard[x, y] = newboard[x, y], newboard[i, j]

            results.append(newboard)
            newboard = np.copy(board)

    return results
