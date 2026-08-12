import streamlit as st
from src.agent import CloudShieldAgent, AutoPilotAgent
from src.orchestrator import Orchestrator
from src.routing import shortest_path
from src.logging_setup import setup_logging

setup_logging()

st.set_page_config(page_title="Sentinel AI India", page_icon="🛰", layout="wide")


def render_home():
    st.info("Home page — coming in C14")


def render_command_centre():
    st.title("🛰 Sentinel AI India — Command Centre")
    st.caption("Real-Time Multi-Agent Monitoring Dashboard")

    st.divider()
    st.subheader("📊 Command Centre Charts")

    import matplotlib.pyplot as plt
    import random as rnd

    rnd.seed(1)
    queue_depths = [rnd.randint(0, 15) for _ in range(20)]  # nosec B311
    tasks_per_agent = {"CloudShield": 11, "AutoPilot": 2, "Sentinel": 7}
    response_times = [120, 340, 89, 560, 210, 45, 670, 130, 290, 88]

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.patch.set_alpha(0)

    for ax in axes.flat:
        ax.set_facecolor("none")
        ax.tick_params(colors="#888888")
        for spine in ["bottom", "left"]:
            ax.spines[spine].set_color("#888888")
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)

    axes[0, 0].plot(queue_depths, color="#5aa9ff", linewidth=2)
    axes[0, 0].set_title("Queue Depth", color="#888888")

    axes[0, 1].bar(tasks_per_agent.keys(), tasks_per_agent.values(), color="#5aa9ff")
    axes[0, 1].set_title("Tasks per Agent", color="#888888")

    axes[1, 0].hist(response_times, bins=5, color="#5aa9ff")
    axes[1, 0].set_title("Response Time Distribution", color="#888888")

    axes[1, 1].plot(sorted(response_times), color="#5aa9ff", linewidth=2)
    axes[1, 1].set_title("Sorted Response Times", color="#888888")

    fig.tight_layout()
    st.pyplot(fig, transparent=True)

    st.divider()
    st.subheader("📦 Response Time Spread by Agent")

    import seaborn as sns
    import pandas as pd

    response_times_by_agent = {
        "CloudShield": [120, 340, 560, 210, 670],
        "AutoPilot": [89, 130, 88],
        "Sentinel": [290, 45, 210, 340],
    }

    rows = []
    for agent, times in response_times_by_agent.items():
        for t in times:
            rows.append({"agent": agent, "response_ms": t})

    df = pd.DataFrame(rows)

    fig_box, ax_box = plt.subplots()
    fig_box.patch.set_alpha(0)
    ax_box.set_facecolor("none")

    sns.boxplot(data=df, x="agent", y="response_ms", ax=ax_box, color="#5aa9ff")

    ax_box.set_title("Response Time Spread by Agent", color="#888888")
    ax_box.tick_params(colors="#888888")
    for spine in ["top", "right"]:
        ax_box.spines[spine].set_visible(False)
    for spine in ["bottom", "left"]:
        ax_box.spines[spine].set_color("#888888")

    mean_val = df["response_ms"].mean()
    ax_box.axhline(
        mean_val,
        color="#ff6b6b",
        linestyle="--",
        label=f"Overall mean: {mean_val:.0f}ms",
    )
    ax_box.legend()

    st.pyplot(fig_box, transparent=True)

    st.divider()
    st.subheader("📈 Interactive Queue Depth (Plotly)")

    import plotly.graph_objects as go

    fig_plotly = go.Figure()
    fig_plotly.add_trace(
        go.Scatter(
            x=list(range(len(queue_depths))),
            y=queue_depths,
            mode="lines+markers",
            line=dict(color="#5aa9ff", width=2),
            name="Queue Depth",
        )
    )

    fig_plotly.update_layout(
        title="Queue Depth (Interactive)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#888888"),
    )

    st.plotly_chart(fig_plotly, use_container_width=True)

    cloudshield = CloudShieldAgent("CloudShield")
    autopilot = AutoPilotAgent("AutoPilot")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🤖 Active Agents")
        st.write(cloudshield)
        st.write(autopilot)

    orch = Orchestrator()
    orch.add_task(3, "Routine Report")
    orch.add_task(1, "Security Breach!")
    orch.add_task(2, "Dataset Profiling Complete")

    with col2:
        st.subheader("⚡ Priority Queue")
        while True:
            task = orch.next_task()
            if task is None:
                break
            urgency, count, name, trace_id = task
            st.success(f"Priority {urgency} → {name}")

    st.divider()
    st.subheader("📊 System Status")

    from src.clients import get_cloudshield_status, get_autopilot_status

    @st.cache_data(ttl=30)
    def cached_cloudshield_status():
        return get_cloudshield_status()

    @st.cache_data(ttl=30)
    def cached_autopilot_status():
        return get_autopilot_status()

    cs_result = cached_cloudshield_status()
    ap_result = cached_autopilot_status()

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### 🛡 CloudShield")
        if cs_result["status"] == "online":
            st.metric("Alerts", cs_result["data"]["alerts_count"])
            st.caption("Status: 🟢 Online")
        else:
            st.warning("🟡 Degraded — CloudShield unreachable")

    with c2:
        st.markdown("### 🚀 AutoPilot")
        if ap_result["status"] == "online":
            st.metric(
                "Datasets Profiled",
                ap_result["data"]["datasets_profiled"],
            )
            st.caption("Status: 🟢 Online")
        else:
            st.warning("🟡 Degraded — AutoPilot unreachable")

    st.divider()
    st.subheader("🗺 Agent Route Finder")

    graph = {
        "CloudShield": ["Sentinel"],
        "Sentinel": ["CloudShield", "AutoPilot"],
        "AutoPilot": ["Sentinel"],
    }

    left, right = st.columns(2)

    with left:
        from_agent = st.text_input("From Agent", "CloudShield")

    with right:
        to_agent = st.text_input("To Agent", "AutoPilot")

    if st.button("Find Shortest Route", use_container_width=True):
        path = shortest_path(graph, from_agent, to_agent)

        if path:
            st.success(" ➜ ".join(path))
        else:
            st.error("No route found.")


def render_evolution():
    st.info("Evolution page — built in C14")


def render_about():
    st.info("About page — coming in C14")


page = st.sidebar.radio("Navigate", ["Home", "Command Centre", "Evolution", "About"])

if page == "Home":
    render_home()
elif page == "Command Centre":
    render_command_centre()
elif page == "Evolution":
    render_evolution()
else:
    render_about()
