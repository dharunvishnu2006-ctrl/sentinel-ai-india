class AgentRegistry:
    def __init__(self):
        self.agents = []

    def add_agent(self, agent_id, name):
        self.agents.append((agent_id, name))
        self.agents.sort(key=lambda a: a[0])

    def linear_find(self, agent_id):
        comparisons = 0
        for aid, name in self.agents:
            comparisons += 1
            if aid == agent_id:
                return name, comparisons
        return None, comparisons

    def binary_find(self, agent_id):
        comparisons = 0
        low, high = 0, len(self.agents) - 1
        while low <= high:
            mid = (low + high) // 2
            comparisons += 1
            mid_id, mid_name = self.agents[mid]
            if mid_id == agent_id:
                return mid_name, comparisons
            elif mid_id < agent_id:
                low = mid + 1
            else:
                high = mid - 1
        return None, comparisons


def can_handle(capacity, load):
    return capacity >= load


def min_capacity_that_fits(load, max_capacity=1_000_000):
    low, high = 1, max_capacity
    checks = 0
    result = None
    while low <= high:
        mid = (low + high) // 2
        checks += 1
        if can_handle(mid, load):
            result = mid
            high = mid - 1
        else:
            low = mid + 1
    return result, checks


result, checks = min_capacity_that_fits(load=347_000)
print(f"Min capacity: {result}, checks: {checks}")
