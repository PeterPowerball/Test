"""Entry point of Snow-Proof. Sets up the page and the navigation between the three pages.

Run with:  streamlit run streamlit_app.py
"""

import streamlit as st

st.set_page_config(layout="wide", page_title="Snow-Proof", page_icon="🏔️")

pages = [
    st.Page("pages/explore.py", title="Explore", icon="🗺️", default=True),
    st.Page("pages/model.py", title="About our model", icon="🧠"),
    st.Page("pages/about.py", title="About us", icon="👋"),
]
st.navigation(pages).run()
