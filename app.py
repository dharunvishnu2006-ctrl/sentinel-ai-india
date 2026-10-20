import streamlit as st

from src.brand import BRAND, current_version
from src.home_data import system_healthy
from src.logging_setup import setup_logging

COMING_NEXT = [
    "Memory in PostgreSQL and a NumPy routing brain - arrives in v2",
    "SLA-breach prediction - arrives in v3",
    "LLM investigation agents and the human approval gate - arrives in v4",
    "The multi-agent SOC crew - arrives in v5",
]

setup_logging()

st.set_page_config(page_title=BRAND.name, page_icon="🛰", layout="wide")

pages = [
    st.Page("views/home.py", title="Home", default=True),
    st.Page("views/command_centre.py", title="Command Centre"),
    st.Page("views/evolution.py", title="Evolution"),
    st.Page("views/about.py", title="About"),
]
page = st.navigation(pages)

with st.sidebar:
    with st.expander(f"Coming next - {len(COMING_NEXT)} modules"):
        st.markdown("\n".join(f"- {line}" for line in COMING_NEXT))
    health = "healthy" if system_healthy() else "unhealthy"
    st.caption(f"{BRAND.name} {current_version()} · System {health}")

page.run()
