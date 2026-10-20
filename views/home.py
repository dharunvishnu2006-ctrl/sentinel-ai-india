import streamlit as st

from src.brand import BRAND, current_version, today_line
from src.home_data import (
    agents_registered,
    build_registry,
    load_task_history,
    route_map_dot,
    systems_online,
    tasks_recorded,
    tests_passing,
)
from src.orchestrator import Orchestrator
from views.shared import cached_system_checks, status_line

REPO = "https://github.com/dharunvishnu2006-ctrl"
SYSTEMS = {
    "CloudShield": ("log-based cloud security", f"{REPO}/cloudshield-x"),
    "AutoPilot": ("MLOps platform", f"{REPO}/autopilot-ml-x"),
}

version = current_version()
st.title(BRAND.name)
st.markdown(f"#### Vision: {BRAND.vision}")
st.markdown(f":orange[**{today_line(version)}**]")

checks = cached_system_checks()
history = load_task_history()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Agents registered", agents_registered(build_registry()))
k2.metric(
    "Connected systems online",
    f"{systems_online(checks)} of {len(checks)}",
)
k3.metric("Tasks recorded", tasks_recorded(history))
k4.metric(f"Tests passing (recorded for {version})", tests_passing())

left, right = st.columns(2)
with left:
    st.subheader("Agent route map")
    st.graphviz_chart(route_map_dot(), width="content")
with right:
    st.subheader("Connected systems")
    for check in checks:
        what, repo = SYSTEMS[check["name"]]
        st.markdown(
            f"**{check['name']}** - {what} · [repo]({repo})  \n" f"{status_line(check)}"
        )
    st.caption(
        "These services run locally; on the live demo they show as " "not reachable."
    )

left, right = st.columns(2)
with left:
    st.subheader("Try the orchestrator")
    st.caption("Your test tasks - not live alerts")
    if "test_orch" not in st.session_state:
        st.session_state.test_orch = Orchestrator()
    orch = st.session_state.test_orch
    with st.form("try_orchestrator", clear_on_submit=True):
        name = st.text_input("Task name", "Test task")
        urgency = st.slider("Urgency (1 = most urgent)", 1, 5, 3)
        if st.form_submit_button("Add task"):
            orch.add_task(urgency, name or "Test task")
    # List queue in pop order.
    queue = sorted(orch.tasks)
    if queue:
        st.markdown(
            "\n".join(
                f"{i}. Urgency {u} - {task}"
                for i, (u, _, task, _) in enumerate(queue, start=1)
            )
        )
    else:
        st.caption("Add a task to see the queue order.")
with right:
    st.subheader("Task history")
    if history:
        st.dataframe(history, hide_index=True)
        st.caption("Tasks recorded during development runs - not live alerts")
    else:
        st.caption("No tasks recorded yet.")

st.divider()
st.caption("Every action will wait for a human - from v4.")
