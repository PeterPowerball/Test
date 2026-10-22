"""
streamlit_app.py: entry point. Page settings and navigation between the pages.

Owner:       Fabio (Task 2: technical foundation, Task 12: integration)
Depends on:  pages/*.py, config.py
Used by:     "streamlit run streamlit_app.py" locally and on Streamlit Community Cloud
Flow:        app (the scripts in scripts/ must have run before, once USE_MOCK_DATA is False)
"""

import streamlit as st

from snowproof import config

st.set_page_config(layout="wide", page_title="Snow-Proof", page_icon="🏔️")

pages = [
    st.Page("pages/explore.py", title="Explore", icon="🗺️", default=True),
    st.Page("pages/model.py", title="About our model", icon="🧠"),
    st.Page("pages/about.py", title="About us", icon="👋"),
]
if config.SHOW_FUTURE_PAGE:  # optional Use Case 2
    pages.append(st.Page("pages/future.py", title="Future outlook", icon="🔭"))

st.navigation(pages).run()
