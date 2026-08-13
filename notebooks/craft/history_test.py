import time
import sys
from src.history import RecentActionsCache
from src.history import UndoStack

sys.path.insert(0, ".")  # noqa: E402
from src.history import SinglyLinkedList  # noqa: E402

N = 100_000

start = time.perf_counter()
linked = SinglyLinkedList()
for i in range(N):
    linked.insert_at_head(i)
time_linked = time.perf_counter() - start

start = time.perf_counter()
py_list: list = []
for i in range(N):
    py_list.insert(0, i)
time_pylist = time.perf_counter() - start

result_steps = linked.search(0)
print(f"Steps to find value 0 (searched last): {result_steps}")

cache = RecentActionsCache(capacity=5)
for i in range(8):
    cache.add_action(f"action-{i}")

print("Forward (newest first):", cache.walk_forward())
print("Backward (oldest first):", cache.walk_backward())

task_assignments = {"task-1": "CloudShield"}
undo_stack = UndoStack()


def reassign(task_id, new_agent):
    old_agent = task_assignments[task_id]

    def reverse():
        task_assignments[task_id] = old_agent
        print(f"Undone: {task_id} back to {old_agent}")

    task_assignments[task_id] = new_agent
    undo_stack.push(f"reassign {task_id} to {new_agent}", reverse)
    print(f"Reassigned {task_id} to {new_agent}")


reassign("task-1", "AutoPilot")
print("Current state:", task_assignments)

undo_stack.undo()
print("After undo:", task_assignments)

result = undo_stack.undo()
print("Second undo (nothing left):", result)
