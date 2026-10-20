import streamlit as st

from src.home_data import (
    ROUTE_GRAPH,
    build_agents,
    load_task_history,
    urgency_counts,
)
from src.orchestrator import Orchestrator
from src.routing import shortest_path
from views.shared import cached_system_checks, status_line

ONLINE_METRICS = {
    "CloudShield": ("Alerts", "alerts_count"),
    "AutoPilot": ("Datasets Profiled", "datasets_profiled"),
}

st.title("🛰 Sentinel AI India — Command Centre")
st.caption("Multi-agent monitoring from the running system")

st.divider()
st.subheader("📊 Telemetry")
history = load_task_history()
if history:
    st.caption("Recorded tasks per urgency, from task_history.csv")
    st.bar_chart(
        urgency_counts(history),
        x="Urgency",
        y="Tasks",
        height=220,
    )
else:
    st.info("Telemetry appears as real tasks are recorded.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🤖 Active Agents")
    for agent in build_agents():
        st.write(agent)

orch = Orchestrator()
orch.add_task(3, "Routine Report")
orch.add_task(1, "Security Breach!")
orch.add_task(2, "Dataset Profiling Complete")

with col2:
    st.subheader("⚡ Priority Queue")
    st.caption("Example tasks - created in code at start")
    while True:
        task = orch.next_task()
        if task is None:
            break
        urgency, count, name, trace_id = task
        st.success(f"Priority {urgency} → {name}")

st.divider()
st.subheader("📊 System Status")

c1, c2 = st.columns(2)
for col, check in zip((c1, c2), cached_system_checks()):
    with col:
        st.markdown(f"### {check['name']}")
        if check["status"] == "online":
            label, key = ONLINE_METRICS[check["name"]]
            st.metric(label, check["data"][key])
        st.caption(f"Status: {status_line(check)}")

st.divider()
st.subheader("🗺 Agent Route Finder")

left, right = st.columns(2)

with left:
    from_agent = st.text_input("From Agent", "CloudShield")

with right:
    to_agent = st.text_input("To Agent", "AutoPilot")

if st.button("Find Shortest Route", width="stretch"):
    path = shortest_path(ROUTE_GRAPH, from_agent, to_agent)

    if path:
        st.success(" ➜ ".join(path))
    else:
        st.error("No route found.")
