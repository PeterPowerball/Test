"""
model.py: the "About our model" page. Data sources, target, inputs, walk-forward validation.

Owner:       Noah (Task 10 and 11) for the layout, Julian (Task 7) for the content and numbers
Depends on:  data_access.get_validation_results(), ui_components.py, config.py
Used by:     streamlit_app.py (navigation)
Flow:        app. Important for grading: this page explains our own ML model.
"""

import streamlit as st

from snowproof import config, data_access
from snowproof import ui_components as ui

st.title("About our model")
if config.USE_MOCK_DATA:
    st.caption("The validation numbers are mock data until our model is trained.")

# ============================================================================ 1. target
st.subheader("1. What we predict")
st.markdown(
    f"A **good ski week** means at least **{config.GOOD_SNOW_CM} cm** of measured snow depth on "
    f"**all {config.GOOD_WEEK_DAYS} days** at the linked measurement station."
)
ui.todo_box("Target explanation", "Julian + Noah", "Task 7 and 10",
            "Explain in 2 to 3 friendly sentences why we use measured snow depth, and that weeks with "
            "missing days are 'unknown' and not used for training.")

# ============================================================================ 2. data sources
st.subheader("2. Where the data comes from")
ui.todo_box("Data sources", "Noah + Nico", "Task 10 and 3",
            "A small table in friendly words: OpenStreetMap (resorts, pistes, lifts), swisstopo (places, "
            "altitude), MeteoSwiss (measured snow depth), Open-Meteo ERA5 (weather), transport.opendata.ch "
            "(travel time), OpenHolidays (school holidays).")

# ============================================================================ 3. inputs
st.subheader("3. What the model knows in advance")
ui.todo_box("Model inputs", "Julian", "Task 6",
            "List the features from snowproof/ml/features.py (FEATURE_COLUMNS) and explain why the weather "
            "of the holiday week itself is NOT an input (data leakage).")

# ============================================================================ 4. validation
st.subheader("4. How we check that it works")
results = data_access.get_validation_results()
try:
    st.plotly_chart(ui.walk_forward_timeline(results), width="stretch")
except NotImplementedError:
    ui.todo_box("Walk-forward timeline", "Noah + Julian", "Task 11 and 7",
                "Train and test periods per round as bars on a year axis.", preview=results)

# ============================================================================ 5. results
st.subheader("5. Results: our model versus the historical baseline")
try:
    left, right = st.columns(2)
    with left:
        st.plotly_chart(ui.model_vs_baseline_chart(results, "model_accuracy", "baseline_accuracy",
                                                   "Accuracy (higher is better)"), width="stretch")
    with right:
        st.plotly_chart(ui.model_vs_baseline_chart(results, "model_brier", "baseline_brier",
                                                   "Brier score (lower is better)"), width="stretch")
except NotImplementedError:
    ui.todo_box("Model versus baseline", "Noah", "Task 11",
                "A results table and two grouped bar charts (accuracy and Brier score) per round.",
                preview=results)
