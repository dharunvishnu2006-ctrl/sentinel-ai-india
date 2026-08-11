import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import random
import seaborn as sns

random.seed(1)
# Fake demo data for chart placeholder - not security-sensitive
queue_depths = [random.randint(0, 15) for _ in range(20)]  # nosec B311

fig, ax = plt.subplots()
ax.plot(queue_depths, color="black")
ax.set_title("Queue Depth Over Time")
fig.savefig("notebooks/craft/chart_wrong.png")
print("Saved chart_wrong.png")

fig2, ax2 = plt.subplots()
fig2.patch.set_alpha(0)
ax2.set_facecolor("none")
ax2.plot(queue_depths, color="#5aa9ff", linewidth=2)
ax2.set_title("Queue Depth Over Time", color="#888888")
ax2.tick_params(colors="#888888")
ax2.spines["bottom"].set_color("#888888")
ax2.spines["left"].set_color("#888888")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
fig2.savefig("notebooks/craft/chart_transparent.png", transparent=True)
print("Saved chart_transparent.png")

tasks_per_agent = {"CloudShield": 11, "AutoPilot": 2, "Sentinel": 7}
response_times = [120, 340, 89, 560, 210, 45, 670, 130, 290, 88]

fig3, axes = plt.subplots(2, 2, figsize=(10, 8))
fig3.patch.set_alpha(0)

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

fig3.tight_layout()
fig3.savefig("notebooks/craft/chart_subplots.png", transparent=True)
print("Saved chart_subplots.png")

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

fig4, ax4 = plt.subplots()
fig4.patch.set_alpha(0)
ax4.set_facecolor("none")

sns.boxplot(data=df, x="agent", y="response_ms", ax=ax4, color="#5aa9ff")

ax4.set_title("Response Time Spread by Agent", color="#888888")
ax4.tick_params(colors="#888888")
for spine in ["top", "right"]:
    ax4.spines[spine].set_visible(False)
for spine in ["bottom", "left"]:
    ax4.spines[spine].set_color("#888888")

mean_val = df["response_ms"].mean()
ax4.axhline(
    mean_val, color="#ff6b6b", linestyle="--", label=f"Overall mean: {mean_val:.0f}ms"
)
ax4.legend()

fig4.savefig("notebooks/craft/chart_boxplot.png", transparent=True)
print("Saved chart_boxplot.png")

fig5 = go.Figure()
fig5.add_trace(
    go.Scatter(
        x=list(range(len(queue_depths))),
        y=queue_depths,
        mode="lines+markers",
        line=dict(color="#5aa9ff", width=2),
        name="Queue Depth",
    )
)

fig5.update_layout(
    title="Queue Depth (Interactive)",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#888888"),
)

fig5.write_html("notebooks/craft/chart_plotly.html")
print("Saved chart_plotly.html")
