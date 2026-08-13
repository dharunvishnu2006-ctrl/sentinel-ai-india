import sys

sys.path.insert(0, ".")  # noqa: E402
from src.routing_advanced import (  # noqa: E402
    bfs_shortest_path,
    dijkstra,
    bellman_ford,
    floyd_warshall,
)

weighted_graph = {
    "Sentinel": {"A": 250, "X": 30},
    "A": {"Target": 250},
    "X": {"Y": 30},
    "Y": {"Target": 30},
    "Target": {},
}

bfs_result = bfs_shortest_path(weighted_graph, "Sentinel", "Target")
print("BFS route:", bfs_result)

dijkstra_result, dijkstra_cost = dijkstra(weighted_graph, "Sentinel", "Target")
print("Dijkstra route:", dijkstra_result, "cost:", dijkstra_cost)

cycle_graph = {
    "A": {"B": 1},
    "B": {"C": -2},
    "C": {"A": -2},
}
distances, has_cycle = bellman_ford(cycle_graph, "A")
print("Negative cycle detected:", has_cycle)

full_table = floyd_warshall(weighted_graph)
print("All-pairs table for Sentinel:", full_table["Sentinel"])
