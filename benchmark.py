import numpy as np
from fifteen import BLANK
from fifteen import solve, solve2
import timeit


if __name__ == "__main__":
    numtests = 3
    easyboard = np.array([[1, 2, 3, 4],
                          [5, 6, 7, 8],
                          [9, 10, 11, 12],
                          [13, 14, BLANK, 15]], dtype=np.int8)
    board = np.array([[5, 1, 2, 4],
                    [9, 6, 3, 8],
                    [BLANK, 14, 7, 11],
                    [10, 13, 15, 12]],
                    dtype=np.int8)
    hardboard = np.array([[5, 1, 6, 4],
                          [9, 3, 2, 7],
                          [BLANK, 14, 15, 8],
                          [10, 13, 12, 11]],
                         dtype=np.int8)
    tests = {
        "Trivial case, pure python.": timeit.timeit(lambda: solve(easyboard), number=numtests) / numtests,
        "Average case, pure python.": timeit.timeit(lambda: solve(board), number=numtests) / numtests,
        "Average case, cython.": timeit.timeit(lambda: solve2(board), number=numtests) / numtests,
        "Hard case, pure python.": timeit.timeit(lambda: solve(hardboard), number=numtests) / numtests,
        "Hard case, cython.": timeit.timeit(lambda: solve2(hardboard), number=numtests) / numtests,
    }

    for desc, t in sorted(tests.items(), key=lambda x: x[1]):
        print desc, t
