import streamlit as st

from src.versions import bug_lines, current_version

st.title("ℹ️ About Sentinel AI India")

st.subheader("Tech Stack")
st.markdown(
    "Python · Streamlit · Pydantic · Flask · Matplotlib · "
    "Seaborn · Plotly · pandas · NumPy · pytest · Bandit"
)

st.subheader("The audit story")
st.markdown(
    "v1 shipped in three days using 26 of its 133 assigned "
    "roadmap steps. v1.1 audited that gap and closed it — "
    "every step from 1 to 133 is now genuinely built, "
    "including a live routing bug (BFS treating every hop "
    "as equal) found and fixed with Dijkstra."
)

v = current_version()
st.subheader(f"Bugs fixed in {v['version']}")
for line in bug_lines(v):
    st.markdown(line)

st.subheader("Links")
st.markdown(
    "[GitHub Repository]" "(https://github.com/dharunvishnu2006-ctrl/sentinel-ai-india)"
)
