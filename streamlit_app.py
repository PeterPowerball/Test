"""
streamlit_app.py: entry point. Page settings and navigation between the pages.

Owner:       Fabio (Task 2: technical foundation, Task 12: integration)
Depends on:  pages/*.py
Used by:     "streamlit run streamlit_app.py" locally and on Streamlit Community Cloud
Flow:        app (pipeline.py must have run before, once USE_MOCK_DATA is False)
"""

import streamlit as st

st.set_page_config(layout="wide", page_title="Snow-Proof", page_icon="🏔️")

pages = [
    st.Page("pages/explore.py", title="Explore", icon="🗺️", default=True),
    st.Page("pages/about_model.py", title="About our model", icon="🧠"),
    st.Page("pages/about_us.py", title="About us", icon="👋"),
]
st.navigation(pages).run()
