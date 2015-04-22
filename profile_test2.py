import numpy as np
from fifteen import BLANK, solve2

if __name__ == "__main__":
    board = np.array([[14, 9, 5, 8],
                      [1, 15, 4, 2],
                      [6, BLANK, 3, 11],
                      [10, 7, 13, 12]],
                     dtype=np.int8)

    for _ in range(10):
        solve2(board)
