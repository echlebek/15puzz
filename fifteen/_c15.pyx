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

cdef struct index:
    int x
    int y

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
    cdef index find_result

    for i in range(4):
        for j in range(4):
            find_result = find(SOLVED, board[i, j])
            x = find_result.x
            y = find_result.y
            result += abs(i - x) + abs(j - y)

    return result


@cython.profile(False)
cdef inline index find(np.ndarray[np.int8_t, ndim=2] board, np.int8_t value):
    """`find` finds the indices of `value` in `board` and stores them in `result`."""
    cdef int i, j
    cdef index result
    for i in range(4):
        for j in range(4):
            if board[i, j] == value:
                # find will always find the value; the caller's risk to take.
                result.x = i
                result.y = j
                return result


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

        if solved(node.board, SOLVED):
            return node

        visited.add(str(node.board.data))

        for m in moves2(node.board):
            cost = manhattan_distance(m)
            if str(m.data) not in visited:
                queue.put(Node(node.distance + 1, cost, m, node))


cdef bint solved(np.ndarray[np.int8_t, ndim=2] board,
                 np.ndarray[np.int8_t, ndim=2] solved_board):
    """`solved` checks to see if the board in question is the solution."""
    cdef int i, j
    for i in range(4):
        for j in range(4):
            if board[i, j] != solved_board[i, j]:
                return False
    return True


cdef list moves2(np.ndarray[np.int8_t, ndim=2] board):
    """
    `moves` generates the next set of moves for the given board.
    """
    cdef int i, j, x, y
    cdef index find_result
    cdef np.ndarray[np.int8_t, ndim=2] newboard
    cdef index[4] moves = [index(0, 1), index(1, 0), index(0, -1), index(-1, 0)]
    cdef np.int8_t t1, t2

    find_result = find(board, BLANK)
    i = find_result.x
    j = find_result.y

    newboard = np.copy(board)
    cdef list results = []

    for m in range(4):
        x = moves[m].x + i
        y = moves[m].y + j
        if x >= 0 and x < 4 and y >= 0 and y < 4:
            # Not all moves are valid, for example if the blank is in the
            # corner, only two moves will be valid.
            t1 = newboard[i, j]
            t2 = newboard[x, y]

            newboard[x, y] = t1
            newboard[i, j] = t2

            results.append(newboard)
            newboard = np.copy(board)

    return results
