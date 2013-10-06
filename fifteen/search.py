from _c15 import moves
from Queue import PriorityQueue
from fifteen import SOLVED, hash_array, SEARCH_LIMIT, Node

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
            if node.distance + 1 < SEARCH_LIMIT and hash_array(m) not in visited:
                queue.put(Node(node.distance + 1, m, node))


def solve(board):
    """
    This is the top level function of the program. `board` is given to the
    search function by placing it into an empty `PriorityQueue`.

    A path to the result is returned.
    """
    start = Node(0, board, None)
    queue = PriorityQueue()
    queue.put(start)
    visited = set()

    result = search(queue, visited)

    def getpath(node, path):
        path.append(node)
        if node.parent is not None:
            return getpath(node.parent, path)
        else:
            return path

    return getpath(result, [])
