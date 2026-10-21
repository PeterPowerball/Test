"""Page 3: Future outlook (Use Case 2). Placeholder with one illustrative chart."""

import streamlit as st

from snowproof import data_access
from snowproof import ui_components as ui

ui.app_header()
st.header("Future outlook")
st.info("Coming later. This page is a sketch of the second use case.")

st.markdown(
    "**The idea:** if you are thinking about buying a holiday home in the mountains, you want to know "
    "how many good ski weeks you can expect in the coming decades. We will show the number of good weeks "
    "per decade until 2050 as a **range across several climate models**."
)

resorts = data_access.get_resorts()
names = dict(zip(resorts["resort_id"], resorts["name"]))
resort_id = st.selectbox("Pick a resort", list(names), format_func=names.get, index=2)

outlook = data_access.get_future_outlook(resort_id)
ui.show_chart(ui.future_range_chart(outlook))
st.caption("Illustration only. These numbers are invented to show the final look and are not a forecast.")
