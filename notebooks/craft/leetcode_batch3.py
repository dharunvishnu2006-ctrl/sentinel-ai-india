import sys

sys.path.insert(0, ".")  # noqa: E402
from src.history import Node  # noqa: E402


def build_list(values):
    head = None
    for v in reversed(values):
        node = Node(v)
        node.next = head
        head = node
    return head


def list_to_array(head):
    result = []
    while head:
        result.append(head.value)
        head = head.next
    return result


def reverse_linked_list(head):
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev


original = build_list([1, 2, 3])
reversed_head = reverse_linked_list(original)
print(list_to_array(reversed_head))


def valid_parentheses(s):
    stack = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for char in s:
        if char in pairs.values():
            stack.append(char)
        else:
            if not stack or stack.pop() != pairs[char]:
                return False
    return not stack


print(valid_parentheses("()[]{}"))
print(valid_parentheses("(]"))
print(valid_parentheses("([)]"))
