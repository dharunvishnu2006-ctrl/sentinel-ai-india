import streamlit as st

from src.home_data import check_systems, display_status


@st.cache_data(ttl=30)
def cached_system_checks():
    return check_systems()


def status_line(check):
    checked = check["checked_at"].strftime("%H:%M:%S")
    return f"{display_status(check['status'])}, checked {checked}"
