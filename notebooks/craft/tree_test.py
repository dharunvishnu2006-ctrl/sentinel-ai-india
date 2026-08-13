import sys

sys.path.insert(0, ".")  # noqa: E402
from src.tree import BST, AVLTree  # noqa: E402

bst_small = BST()
for load in range(500):
    bst_small.insert(load)

print(f"Depth after 500 ascending inserts: {bst_small.depth()}")

avl = AVLTree()
for load in range(500):
    avl.insert(load)

print(f"AVL depth after 500 ascending inserts: {avl.depth()}")
