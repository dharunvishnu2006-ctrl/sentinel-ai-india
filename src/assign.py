class Agent:
    def __init__(self, name, capabilities):
        self.name = name
        self.capabilities = capabilities


def greedy_assign(tasks, agents):
    available = agents.copy()
    assignments = {}
    for task_name, required_capability in tasks:
        assigned = None
        for agent in available:
            if required_capability in agent.capabilities:
                assigned = agent
                break
        if assigned:
            assignments[task_name] = assigned.name
            available.remove(assigned)
        else:
            assignments[task_name] = None
    return assignments


def backtracking_assign(tasks, agents, index=0, assignments=None):
    if assignments is None:
        assignments = {}
    if index == len(tasks):
        return assignments

    task_name, required_capability = tasks[index]
    for agent in agents:
        if (
            agent.name not in assignments.values()
            and required_capability in agent.capabilities
        ):
            assignments[task_name] = agent.name
            result = backtracking_assign(tasks, agents, index + 1, assignments)
            if result is not None and all(v is not None for v in result.values()):
                return result
            del assignments[task_name]

    assignments[task_name] = None
    return assignments
