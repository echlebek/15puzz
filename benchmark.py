import numpy as np
from fifteen import BLANK
from fifteen import solve, solve2
import timeit


if __name__ == "__main__":
    numtests = 5
    board = np.array([[5, 1, 2, 4],
                    [9, 6, 3, 8],
                    [10, 14, 7, 11],
                    [13, BLANK, 15, 12]],
                    dtype=np.uint8)
    def s1():
        solve(board)

    print "solve1", timeit.timeit(s1, number=numtests) / numtests

    def s2():
        solve2(board)

    print "solve2", timeit.timeit(s2, number=5) / numtests
