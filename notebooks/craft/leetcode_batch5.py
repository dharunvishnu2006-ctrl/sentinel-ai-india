import sys

sys.path.insert(0, ".")  # noqa: E402
from src.topology import topological_sort  # noqa: E402


def num_islands(grid):
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    islands = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return

        grid[r][c] = "0"

        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                islands += 1
                dfs(r, c)

    return islands


grid = [
    ["1", "1", "0", "0"],
    ["1", "1", "0", "0"],
    ["0", "0", "1", "0"],
    ["0", "0", "0", "1"],
]
print(num_islands(grid))


def can_finish(numCourses, prerequisites):
    graph = {i: [] for i in range(numCourses)}
    for course, prerequisite in prerequisites:
        graph[course].append(prerequisite)
    order = topological_sort(graph)
    return order is not None


print(can_finish(2, [[1, 0]]))
print(can_finish(2, [[1, 0], [0, 1]]))
