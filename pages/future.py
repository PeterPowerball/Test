"""
future.py: OPTIONAL "Future outlook" page (Use Case 2). Only built if time allows.

Owner:       Everyone, later (only after everything else works)
Depends on:  config.SHOW_FUTURE_PAGE (the page is hidden while this is False)
Used by:     streamlit_app.py (navigation, only when config.SHOW_FUTURE_PAGE is True)
Flow:        app, after the main use case is finished

Idea: for people buying a holiday home, show the number of good ski weeks per decade
until 2050 as a range across several climate models.
"""

import streamlit as st

from snowproof import ui_components as ui

st.title("Future outlook")
st.info("Coming later. This page is optional.")

ui.todo_box("Climate projections (optional)", "Everyone", "later",
            "Find climate scenario data for Switzerland (e.g. CH2018 or CMIP6), apply our model to "
            "several climate models, and show good ski weeks per decade until 2050 as a range band.")

# TODO [ALL | optional] Seasonal forecasts (ECMWF)
# Our tutor advised against making seasonal forecasts a main point. Only look at this if
# everything else is finished, and discuss it with the tutor first.
ui.todo_box("Seasonal forecast (optional, not planned)", "Everyone", "later",
            "Our tutor advised against this. Only consider it after everything else works.")
