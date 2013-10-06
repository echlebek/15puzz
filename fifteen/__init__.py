import numpy as np
from collections import namedtuple

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


def hash_array(array):
    """Gives the hashed result of a numpy array."""
    return tuple(array.flat)
