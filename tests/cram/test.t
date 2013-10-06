  $ cat > test.py <<EOF
  > import numpy as np
  > from fifteen import BLANK, solve
  > if __name__ == "__main__":
  >     board = np.array([[5, 1, 2, 4],
  >                       [9, 6, 3, 8],
  >                       [10, 14, 7, 11],
  >                       [13, BLANK, 15, 12]],
  >                     dtype=np.uint8)
  >     solve(board)
  > EOF

  $ ls test.py
  test.py
  $ python test.py
