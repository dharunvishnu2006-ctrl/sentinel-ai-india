import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis("off")

boxes = {
    "Streamlit\nDashboard": (5, 7),
    "CloudShieldAgent": (1.5, 5),
    "AutoPilotAgent": (5, 5),
    "Orchestrator\n(heap)": (8.5, 5),
    "src/clients.py\n(HTTP + retry)": (1.5, 3),
    "src/routing.py\n(BFS)": (5, 3),
    "sentinel.log\n(JSON)": (8.5, 3),
    "CloudShield API\n(external)": (0.5, 1),
    "AutoPilot API\n(external)": (2.5, 1),
}

for label, (x, y) in boxes.items():
    box = mpatches.FancyBboxPatch(
        (x - 0.9, y - 0.5),
        1.8,
        1,
        boxstyle="round,pad=0.1",
        edgecolor="#5aa9ff",
        facecolor="none",
        linewidth=2,
    )
    ax.add_patch(box)
    ax.text(x, y, label, ha="center", va="center", fontsize=9)

arrows = [
    ("Streamlit\nDashboard", "CloudShieldAgent"),
    ("Streamlit\nDashboard", "AutoPilotAgent"),
    ("Streamlit\nDashboard", "Orchestrator\n(heap)"),
    ("Streamlit\nDashboard", "src/routing.py\n(BFS)"),
    ("CloudShieldAgent", "sentinel.log\n(JSON)"),
    ("AutoPilotAgent", "sentinel.log\n(JSON)"),
    ("Orchestrator\n(heap)", "sentinel.log\n(JSON)"),
    ("Streamlit\nDashboard", "src/clients.py\n(HTTP + retry)"),
    ("src/clients.py\n(HTTP + retry)", "CloudShield API\n(external)"),
    ("src/clients.py\n(HTTP + retry)", "AutoPilot API\n(external)"),
]

for start, end in arrows:
    x1, y1 = boxes[start]
    x2, y2 = boxes[end]
    ax.annotate(
        "",
        xy=(x2, y2 + 0.5),
        xytext=(x1, y1 - 0.5),
        arrowprops=dict(arrowstyle="->", color="#888888", lw=1.5),
    )

ax.set_title(
    "Sentinel AI India — Architecture (v1.1)",
    fontsize=14,
    color="#333333",
)

fig.savefig("docs/architecture.png", dpi=150, bbox_inches="tight")
print("Saved architecture.png")
