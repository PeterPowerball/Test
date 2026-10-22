"""Page 2: About our model. A short, visual explanation of how the prediction works."""

import streamlit as st

from snowproof import config, data_access
from snowproof import ui_components as ui

ui.app_header()
st.header("About our model")
st.caption("The validation numbers below are mock data until our model is trained.")

st.subheader("1. What we predict")
st.markdown(
    f"A **good ski week** means at least **{config.GOOD_SNOW_CM} cm** of snow depth on "
    f"**all {config.GOOD_WEEK_DAYS} days** at the linked measurement station. "
    "The model answers one yes/no question and gives you the probability of a yes."
)

st.subheader("2. Where the data comes from")
st.table({
    "What": ["Ski resorts, slopes, lifts", "Altitudes and your address", "Measured snow depth",
             "Weather features", "Travel time", "School holidays"],
    "Source": ["OpenStreetMap", "swisstopo", "MeteoSwiss Open Data", "Open-Meteo Historical (ERA5)",
               "transport.opendata.ch", "OpenHolidays API"],
})

st.subheader("3. What the model knows in advance")
left, right = st.columns(2)
with left:
    st.markdown("**Always**\n- Altitude of the station\n- Week of the season\n- Region\n"
                "- Long-term warming trend\n- Past snow history for this week")
with right:
    st.markdown("**During the season (extra)**\n- Current snow depth\n- Recent snowfall")

st.subheader("4. How we check that it works")
st.markdown(
    "We never test on data the model has seen. In **walk-forward validation** the model is trained "
    "on the past and tested on the next decade, then the training period grows. "
    "The final check (2015 to 2025) is never used for tuning."
)
results = data_access.get_validation_results()
ui.show_chart(ui.walk_forward_timeline(results))

st.subheader("5. Results (mock)")
st.dataframe(
    results.rename(columns={
        "round": "Round", "train_period": "Train", "test_period": "Test",
        "model_accuracy": "Model accuracy", "baseline_accuracy": "Baseline accuracy",
        "model_brier": "Model Brier", "baseline_brier": "Baseline Brier"}),
    hide_index=True, width="stretch",
)
st.caption("Accuracy: higher is better. Brier score: lower is better. "
           "The baseline simply uses the historical share of good weeks.")
c1, c2 = st.columns(2)
with c1:
    ui.show_chart(ui.model_vs_baseline_chart(results, "model_accuracy", "baseline_accuracy", "Accuracy (higher is better)"))
with c2:
    ui.show_chart(ui.model_vs_baseline_chart(results, "model_brier", "baseline_brier", "Brier score (lower is better)"))
