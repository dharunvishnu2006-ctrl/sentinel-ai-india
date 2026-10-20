# Sentinel AI India

Security command-centre software built one version at a time: it keeps a
list of its agents, sorts tasks by urgency, finds the shortest route between
agents, and checks whether CloudShield X and AutoPilot ML X are online.
Its agents are Python classes today; LLM agents arrive in v4.

**Live demo:** https://sentinel-ai-india.streamlit.app
**Repository:** https://github.com/dharunvishnu2006-ctrl/sentinel-ai-india

![version](https://img.shields.io/badge/version-v1.1-B45309) ![tests](https://img.shields.io/badge/tests-80%20passed-brightgreen) ![python](https://img.shields.io/badge/python-3.14-blue)

## What it does

- Keeps a registry of its agents and finds one by id with binary search.
- Sorts tasks in a priority queue: the most urgent goes first. Try it on
  the Home page; your test tasks stay in your browser session.
- Finds the shortest route between agents with BFS (every link is one hop).
- Checks CloudShield X and AutoPilot ML X through their REST APIs and says
  "online" or "not reachable", with the time checked.
- Records each handled task with a trace id in task_history.csv.

## What's new in v1.1

v1.1 built all 133 roadmap steps (v1 had used 26): typed records and
validation, JSON logs with trace ids, an agent class hierarchy, REST clients
for both flagships, the agent registry, task history, and BFS routing, with
Dijkstra, Bellman-Ford and Floyd-Warshall written and tested. The home page
polish (20 October 2026) replaced the Command Centre's typed-in charts with
numbers from the running system and removed all HTML.

## Run it

    pip install -r requirements.txt
    streamlit run app.py
    pytest -q

## Numbers

| What | Value |
|---|---|
| Tests | 80 passed in 27.68 s (pytest -q) |
| Roadmap steps built | 133 of 600 |
| Agents registered | 2 |
| Tasks recorded | 2 (development runs) |

The old Command Centre drew four good-looking charts from numbers typed into
the code; every number on the page now comes from the registry, the status
checks, task_history.csv or versions.json.

## Known limits

No AI yet: the agents are Python classes. The queue lives in memory, so a
restart loses it; only task_history.csv is kept. The Flask /status API has no
authentication. CloudShield X and AutoPilot ML X run locally, so on the live
demo they show as not reachable. The app routes with BFS; Dijkstra is tested
but not yet integrated.

## Built with

v1 and v1.1 were written by hand. The home page polish was built with
Claude Code and Claude: I wrote the spec, checked the plan, ran every check,
and made the accent colour, About text and versions.json changes by hand.
Python, Streamlit, Pydantic, Flask, pandas, NumPy, pytest, Bandit.

Docs: [design](docs/design.md) · [ADRs](docs/adr/) · [build log](docs/build_log.md)

## Versions

| Version | What | Tests |
|---|---|---|
| v1.0 | Foundation: agent backbone sprint | 5 |
| v1.1 | Completion: all 133 steps, honest home page | 80 |
| v2 | Next: memory in PostgreSQL and a NumPy routing brain | |