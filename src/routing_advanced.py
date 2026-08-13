import heapq
from collections import deque


def bfs_shortest_path(graph, start, goal):
    queue = deque([[start]])
    visited = {start}
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == goal:
            return path
        for neighbor in graph.get(node, {}):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return []


def dijkstra(graph, start, goal):
    distances = {node: float("inf") for node in graph}
    distances[start] = 0
    previous = {}
    pq = [(0, start)]
    visited = set()

    while pq:
        current_dist, current_node = heapq.heappop(pq)
        if current_node in visited:
            continue
        visited.add(current_node)

        if current_node == goal:
            break

        for neighbor, weight in graph.get(current_node, {}).items():
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    path = []
    node = goal
    while node in previous:
        path.append(node)
        node = previous[node]
    if node == start:
        path.append(start)
        path.reverse()
        return path, distances[goal]
    return [], float("inf")


def bellman_ford(graph, start):
    distances = {node: float("inf") for node in graph}
    distances[start] = 0

    nodes = list(graph.keys())
    for _ in range(len(nodes) - 1):
        for node in nodes:
            for neighbor, weight in graph.get(node, {}).items():
                if distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight

    for node in nodes:
        for neighbor, weight in graph.get(node, {}).items():
            if distances[node] + weight < distances[neighbor]:
                return distances, True

    return distances, False


def floyd_warshall(graph):
    nodes = list(graph.keys())
    dist = {u: {v: float("inf") for v in nodes} for u in nodes}

    for node in nodes:
        dist[node][node] = 0

    for u in graph:
        for v, weight in graph[u].items():
            dist[u][v] = weight

    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist
