"""Page 3: About us. Who we are and why we built Snow-Proof."""

import streamlit as st

from snowproof import ui_components as ui

ui.app_header()
st.header("About us")

st.markdown(
    "We are five business students at the **University of St. Gallen (HSG)**. Snow-Proof is our group "
    "project for the course *Fundamentals and Methods of Computer Science for Business Studies*."
)

st.subheader("Why Snow-Proof?")
st.markdown(
    "Ski holidays are booked months in advance, but nobody knows if the snow will be good. "
    "Snow-Proof uses decades of measured snow depth to tell you how likely a good ski week is "
    "for your dates and your favorite resort."
)

st.subheader("The team")
team = [
    ("Nico", "Data and database"),
    ("Julian", "Machine learning model"),
    ("Jan", "Machine learning model, filters and ranking"),
    ("Noah", "User interface, map and charts"),
    ("Fabio", "Integration, testing and deployment"),
]
cols = st.columns(len(team))
for col, (name, role) in zip(cols, team):
    with col.container(border=True):
        st.markdown(f"**{name}**")
        st.caption(role)
