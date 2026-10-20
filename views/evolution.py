import streamlit as st

from src.versions import (
    bug_lines,
    feature_lines,
    load_versions,
    total_roadmap_steps,
)

st.title("📈 How Sentinel AI India Grew")
st.caption("Every number on this page comes from versions.json")

try:
    versions = load_versions()
except FileNotFoundError as e:
    st.error(f"versions.json missing: {e}")
    st.stop()

grand_total = total_roadmap_steps(versions)
st.caption(f"Total roadmap: {grand_total} steps, {len(versions)} versions")

cols = st.columns(len(versions))
for i, v in enumerate(versions):
    with cols[i]:
        with st.container(border=True):
            st.markdown(f"**{v['version']}**")
            if v["status"] == "shipped":
                st.progress(
                    v["completion"] / 100,
                    text=f"{v['completion']}%",
                )
                st.caption(f"{v['steps_covered']}/{grand_total} steps")
            else:
                st.caption(f"Planned · steps {v['steps']}")

st.divider()
st.subheader("🔍 Version Detail")
for v in [x for x in versions if x["status"] == "shipped"]:
    header = (
        f"{v['version']} — {v['steps_covered']} steps, "
        f"{len(v['features'])} features, {v['tests']} tests, "
        f"{len(v['bugs_fixed'])} bugs fixed"
    )
    with st.expander(header):
        st.markdown("**Features:**")
        st.markdown("\n".join(feature_lines(v)))
        if v["bugs_fixed"]:
            st.markdown("**Bugs Fixed:**")
            st.markdown("\n".join(bug_lines(v)))

st.divider()
st.subheader("📄 Decisions (ADRs)")
repo = "https://github.com/dharunvishnu2006-ctrl/" "sentinel-ai-india/blob/main"
st.markdown(
    f"- [ADR 001 — itertools counter over trace_id/task "
    f"as heap tie-breaker]"
    f"({repo}/docs/adr/001-heap-tie-breaker.md)\n"
    "- ADR 002 (not written yet)"
)

st.divider()
st.subheader("⚠️ Known Limits")
st.markdown(
    "- Everything is in memory — a restart loses all agent "
    "and task state (v2 adds a database)\n"
    "- Sentinel's Flask API has no authentication on /status\n"
    "- Priority queue is not persisted; Streamlit re-running "
    "the script can duplicate task creation\n"
    "- export_history() writes tasks in heap-priority order, "
    "not insertion order\n"
    "- Retries cannot fix a genuinely down API, only smooth "
    "over brief transient failures\n"
    "- v1.0 and v1.1 share the same step range (1-133); "
    "per-version step counts display independently rather "
    "than as a deduplicated cumulative total"
)
