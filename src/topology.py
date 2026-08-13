class UnionFind:
    def __init__(self, items):
        self.parent = {item: item for item in items}
        self.rank = {item: 0 for item in items}

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return
        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1


def topological_sort(dependencies):
    graph = {}
    in_degree = {}
    for task, deps in dependencies.items():
        graph.setdefault(task, [])
        in_degree.setdefault(task, 0)
        for dep in deps:
            graph.setdefault(dep, []).append(task)
            in_degree[task] = in_degree.get(task, 0) + 1
            in_degree.setdefault(dep, 0)

    queue = [t for t in in_degree if in_degree[t] == 0]
    order = []

    while queue:
        current = queue.pop(0)
        order.append(current)
        for neighbor in graph.get(current, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(in_degree):
        return None

    return order
