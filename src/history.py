class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert_at_head(self, value):
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node

    def search(self, target):
        current = self.head
        steps = 0
        while current is not None:
            steps += 1
            if current.value == target:
                return steps
            current = current.next
        return -1


class DoublyNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class RecentActionsCache:
    def __init__(self, capacity=50):
        self.head = None
        self.tail = None
        self.capacity = capacity
        self.size = 0

    def add_action(self, value):
        new_node = DoublyNode(value)
        new_node.next = self.head
        if self.head is not None:
            self.head.prev = new_node
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self.size += 1

        if self.size > self.capacity:
            self.tail = self.tail.prev
            self.tail.next = None
            self.size -= 1

    def walk_forward(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    def walk_backward(self):
        result = []
        current = self.tail
        while current is not None:
            result.append(current.value)
            current = current.prev
        return result


cache = RecentActionsCache(capacity=5)
for i in range(8):
    cache.add_action(f"action-{i}")

print("Forward (newest first):", cache.walk_forward())
print("Backward (oldest first):", cache.walk_backward())


class UndoStack:
    def __init__(self):
        self.stack = []

    def push(self, action, reverse_action):
        self.stack.append((action, reverse_action))

    def undo(self):
        if not self.stack:
            return None
        action, reverse_action = self.stack.pop()
        reverse_action()
        return action
