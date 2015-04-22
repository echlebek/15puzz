# cython: profile=False
import numpy as np
cimport numpy as np
from collections import namedtuple
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


cdef int manhattan_distance(np.ndarray[np.int8_t, ndim=2] board,
                            np.ndarray[np.int8_t, ndim=2] solved_board):
    """Manhattan distance finds how many squares out of place each value in
    `board` is. This is also known as "taxicab distance".
    """
    cdef int result = 0
    cdef int i, j
    cdef int x, y

    # For each tile in the game
    for i in range(4):
        for j in range(4):

            # For each tile in the solved game
            for x in range(4):
                for y in range(4):
                    if board[i, j] == solved_board[x, y]:
                        result += abs(i - x) + abs(j - y)
                        break
                else:
                    continue
                break

    return result


cpdef search2(queue, set visited):
    """
    `search` iteratively gets `Node`s out of `queue`, adding them to `visited`
    as it goes. For each item, `moves` is called on the node's board. Each
    move is added to the queue if it is not already in the visited set.
    """
    cdef int i, j, cost
    cdef int iter = 0
    cdef np.ndarray[np.int8_t, ndim=2] solved_board

    solved_board = SOLVED

    while not queue.empty():
        node = queue.get()

        if board_equals(node.board, solved_board):
            return node

        visited.add(str(node.board.data))

        for m in moves2(node.board):
            cost = manhattan_distance(m, solved_board)
            if str(m.data) not in visited:
                queue.put(Node(node.distance + 1, cost, m, node))


cdef bint board_equals(np.ndarray[np.int8_t, ndim=2] a,
                       np.ndarray[np.int8_t, ndim=2] b):
    """`board_equals` checks to see if the boards are equal"""
    cdef int i, j
    for i in range(4):
        for j in range(4):
            if a[i, j] != b[i, j]:
                return False
    return True


cdef list moves2(np.ndarray[np.int8_t, ndim=2] board):
    """
    `moves` generates the next set of moves for the given board.
    """
    cdef int i, j, x, y
    cdef np.ndarray[np.int8_t, ndim=2] newboard
    cdef index[4] moves = [index(0, 1), index(1, 0), index(0, -1), index(-1, 0)]
    cdef np.int8_t t1, t2

    for i in range(4):
        for j in range(4):
            if board[i, j] == BLANK:
                # iteration ends, i and j now point to the blank tile
                break
        else:
            continue
        break

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
