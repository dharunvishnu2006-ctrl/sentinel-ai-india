import sys

sys.path.insert(0, ".")  # noqa: E402
from src.tree import BSTNode  # noqa: E402


def max_depth(root):
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


root = BSTNode(1)
root.left = BSTNode(2)
root.right = BSTNode(3)
root.left.left = BSTNode(4)

print(max_depth(root))


def tree_to_list_bfs(root):
    from collections import deque

    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node:
            result.append(node.value)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    while result and result[-1] is None:
        result.pop()
    return result


def invert_tree(root):
    if root is None:
        return None
    root.left, root.right = root.right, root.left
    invert_tree(root.left)
    invert_tree(root.right)
    return root


tree = BSTNode(4)
tree.left = BSTNode(2)
tree.right = BSTNode(7)
tree.left.left = BSTNode(1)
tree.left.right = BSTNode(3)
tree.right.left = BSTNode(6)
tree.right.right = BSTNode(9)

inverted = invert_tree(tree)
print(tree_to_list_bfs(inverted))
