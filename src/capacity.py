from itertools import combinations

SCAN = 0b001
ROUTE = 0b010
DEPLOY = 0b100


def can_handle(agent_mask, task_mask):
    return (agent_mask & task_mask) == task_mask


def brute_force_knapsack(tasks, capacity):
    best_value = 0
    best_set = []
    for r in range(len(tasks) + 1):
        for subset in combinations(tasks, r):
            total_cost = sum(t[0] for t in subset)
            total_value = sum(t[1] for t in subset)
            if total_cost <= capacity and total_value > best_value:
                best_value = total_value
                best_set = subset
    return best_value, best_set


def knapsack_dp(tasks, capacity):
    n = len(tasks)
    table = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost, value = tasks[i - 1]
        for c in range(capacity + 1):
            if cost > c:
                table[i][c] = table[i - 1][c]
            else:
                table[i][c] = max(
                    table[i - 1][c],
                    table[i - 1][c - cost] + value,
                )

    chosen = []
    c = capacity
    for i in range(n, 0, -1):
        if table[i][c] != table[i - 1][c]:
            cost, value = tasks[i - 1]
            chosen.append(tasks[i - 1])
            c -= cost

    return table[n][capacity], chosen


def urgency_order_selection(tasks, capacity):
    sorted_tasks = sorted(tasks, key=lambda t: -t[1])
    chosen = []
    remaining = capacity
    total_value = 0
    for cost, value in sorted_tasks:
        if cost <= remaining:
            chosen.append((cost, value))
            remaining -= cost
            total_value += value
    return total_value, chosen
