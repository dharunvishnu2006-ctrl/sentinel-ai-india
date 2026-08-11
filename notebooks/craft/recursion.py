team = {
    "name": "CloudShield",
    "children": [
        {
            "name": "Scanner-1",
            "children": [
                {"name": "Scanner-1a", "children": []},
                {"name": "Scanner-1b", "children": []},
            ],
        },
        {
            "name": "Scanner-2",
            "children": [],
        },
    ],
}


def print_team(agent, depth=0):
    print("  " * depth + agent["name"])
    for child in agent["children"]:
        print_team(child, depth + 1)


print_team(team)


def print_team_broken(agent, depth=0):
    for child in agent["children"]:
        print_team_broken(child, depth + 1)
    print("  " * depth + agent["name"])


def print_team_infinite(agent, depth=0):
    print("  " * depth + agent["name"])
    print_team_infinite(agent, depth + 1)


print_team_infinite(team)
