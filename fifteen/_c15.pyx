import numpy as np
cimport numpy as np
from fifteen import BLANK


def moves(np.ndarray board):
    """
    `moves` generates the next set of moves for the given board.
    """
    cdef np.ndarray newboard = np.copy(board)
    cdef int x, y

    ((i,), (j,)) = np.nonzero(board == BLANK)
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for x, y in moves:
        x += i
        y += j

        try:
            newboard[i, j], newboard[x, y] = newboard[x, y], newboard[i, j]
        except IndexError:
            # Not all moves are valid, for example if the blank is in the
            # corner, only two moves will be valid.
            continue

        yield newboard
        newboard = np.copy(board)
