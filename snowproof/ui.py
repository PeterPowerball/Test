"""
ui.py: reusable UI pieces (sidebar, map, resort card, chance bar, charts) and todo_box.

Owner:       Noah (Task 10: user interface and navigation, Task 11: map, charts and resort details)
Depends on:  config.py (colors), data_access.py (only through the pages)
Used by:     pages/explore.py, pages/about_model.py
Flow:        app

Rule: these functions only DRAW. They get their data as arguments from the page,
which got it from data_access.py. They never call an API or the database themselves.

Look at the ui-prototype branch for how each piece should look in the end.
"""

from datetime import date

import folium
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_folium import st_folium

from snowproof import config


# ============================================================================ todo_box
def todo_box(title: str, owner: str, task: str, description: str, preview=None) -> None:
    """
    Show a visible "Under construction" box in the app instead of a section that is not built yet.

    Owner:    Fabio (Task 2), already done. Do not change it, just call it.
    Used by:  every page, in the "except NotImplementedError" part of each section
    Returns:  nothing

    preview:  optional mock data (DataFrame, dict or list) shown in an expander, so the owner
              sees which data the section will get.
    """
    with st.container(border=True):
        st.markdown(f"#### 🚧 Under construction: {title}")
        st.markdown(f"**Owner:** {owner} &nbsp;·&nbsp; **Task:** {task}")
        st.caption(description)
        if preview is not None:
            with st.expander("Mock data this section will use"):
                if isinstance(preview, pd.DataFrame):
                    st.dataframe(preview, hide_index=True)
                else:
                    st.write(preview)


# ============================================================================ sidebar
def sidebar_filters(cantons: list[str], holiday_cantons: list[str]) -> dict:
    """
    Draw the optional filters in the sidebar and return what the user chose.

    Owner:    Noah + Jan (Task 10 and Task 8)
    Used by:  pages/explore.py
    Source:   data_access.get_cantons(), data_access.get_school_holiday_cantons(), get_school_holidays()
    Returns:  dict with keys
                place (str, the city / village, "" if empty), cantons (list[str]),
                max_minutes (float), dates (tuple[date, date] or None if not set or not valid)
    """
    # TODO [NOAH+JAN | Task 10] Sidebar filters
    # Step 1: Inside "with st.sidebar:", add st.text_input("City / village") (no street address, privacy),
    #         st.multiselect("Canton", cantons), and st.slider for the max travel time in hours
    #         (disabled while no city / village is entered).
    # Step 2: Add an st.expander "Use school holidays of a canton" with a selectbox of holiday_cantons
    #         and one button per holiday period. The button sets the date input through
    #         st.session_state (use the button's on_click callback).
    # Step 3: Add st.date_input("Holiday dates", key="holiday_range") for a date range.
    # Step 4: Check the dates with location.validate_holiday_range and show st.sidebar.warning if needed.
    # Hint:   Give every widget a key=..., so its value survives reruns and can be set from callbacks.
    # Hint:   All filters are optional. With nothing filled in, return place="", cantons=[], dates=None.
    # Done when: the sidebar looks like the prototype and the returned dict changes when you use it.
    raise NotImplementedError("TODO [NOAH+JAN | Task 10]: sidebar_filters")


# ============================================================================ map
def build_map(resorts: pd.DataFrame, chances: dict[str, float] | None) -> folium.Map:
    """
    The map of Switzerland with one circle per resort.

    Owner:    Noah (Task 11: map, charts and resort details)
    Used by:  pages/explore.py
    Source:   data_access.get_resorts() (after the filters), chances from get_ranked_resorts()
    Returns:  a folium.Map
    """
    # TODO [NOAH | Task 11] Build the map
    # Step 1: folium.Map(location=config.MAP_CENTER, zoom_start=config.MAP_ZOOM, tiles=None).
    # Step 2: Add the swisstopo tiles: folium.TileLayer(tiles=config.SWISSTOPO_TILES,
    #         attr=config.SWISSTOPO_ATTRIBUTION). Add a fallback layer and folium.LayerControl.
    # Step 3: One folium.CircleMarker per resort, tooltip=resort name, radius growing with total_piste_km.
    # Step 4: Color: config.GREY without station, config.ACCENT_BLUE by default,
    #         traffic light colors (config.GREEN / AMBER / RED) when chances is given.
    # Hint:   Put the color rule in a small helper chance_color(chance) using config.GOOD_CHANCE_MIN
    #         and config.OK_CHANCE_MIN. You need it again for the chance bar.
    # Hint:   Add config.OSM_ATTRIBUTION once the resorts come from OpenStreetMap.
    # Done when: all resorts appear as dots of different sizes, grey ones where there is no station.
    raise NotImplementedError("TODO [NOAH | Task 11]: build_map")


def show_map(fmap: folium.Map, key: str) -> str | None:
    """
    Draw the map and return the name of the resort the user clicked (or None).

    Owner:    Noah (Task 11: map, charts and resort details)
    Used by:  pages/explore.py
    Source:   the map from build_map()
    Returns:  the clicked resort's name (the tooltip text), or None
    """
    # TODO [NOAH | Task 11] Show the map and read clicks
    # Step 1: out = st_folium(fmap, height=520, use_container_width=True, key=key,
    #         returned_objects=["last_object_clicked_tooltip"]).
    #         returned_objects limits reruns to clicks, so panning and zooming stay smooth.
    # Step 2: Return out["last_object_clicked_tooltip"] (strip spaces), or None.
    # Hint:   st_folium keeps returning the LAST click on every rerun. In the page, remember the last
    #         click you handled in st.session_state and only react to a NEW one (see the prototype).
    # Done when: clicking a dot sets st.session_state["selected_resort_id"] and shows the resort card.
    raise NotImplementedError("TODO [NOAH | Task 11]: show_map")


def map_legend(with_chances: bool) -> None:
    """
    Small legend below the map (colors and "circle size = piste km").

    Owner:    Noah (Task 11: map, charts and resort details)
    Used by:  pages/explore.py
    Returns:  nothing
    """
    # TODO [NOAH | Task 11] Map legend
    # Step 1: Without chances: blue = resort with snow data, grey = no station nearby.
    # Step 2: With chances: green / amber / red for the odds, grey = no station.
    # Hint:   st.markdown with small colored dots in HTML (unsafe_allow_html=True) is enough.
    # Done when: the legend matches the colors on the map.
    raise NotImplementedError("TODO [NOAH | Task 11]: map_legend")


def ranked_list(ranked: pd.DataFrame) -> None:
    """
    The ranked list of resorts below the map (only when holiday dates are set).

    Owner:    Noah + Jan (Task 10 and Task 9)
    Used by:  pages/explore.py
    Source:   data_access.get_ranked_resorts()
    Returns:  nothing (a "Select" button per row sets st.session_state["selected_resort_id"])
    """
    # TODO [NOAH+JAN | Task 10] Ranked resort list
    # Step 1: st.subheader("Best resorts for your dates").
    # Step 2: For the top 10 rows: st.columns with name, canton, chance (colored), travel time,
    #         and st.button("Select", key=f"rank_{resort_id}", on_click=..., args=(resort_id,)).
    # Hint:   Every button needs its own key, otherwise Streamlit raises a duplicate key error.
    # Done when: clicking "Select" opens that resort's card.
    raise NotImplementedError("TODO [NOAH+JAN | Task 10]: ranked_list")


# ============================================================================ resort card
def resort_card(details: dict, pistes: pd.DataFrame, station: dict | None,
                travel_minutes: int | None) -> bool:
    """
    The resort details below the map: name, description, key numbers, pistes, station, button.

    Owner:    Noah (Task 11: map, charts and resort details)
    Used by:  pages/explore.py
    Source:   data_access.get_resort_details(), get_pistes(), get_linked_station(), get_travel_time_minutes()
    Returns:  True if the user clicked "Check the snow for your holiday", otherwise False
    """
    # TODO [NOAH | Task 11] Resort card
    # Step 1: In st.container(border=True): st.subheader with name and canton, a "Close" button,
    #         and the description.
    # Step 2: st.metric for piste km, lifts, base altitude and summit altitude (2 columns x 2 rows,
    #         otherwise the numbers get cut off).
    # Step 3: The piste km by difficulty as a horizontal stacked plotly bar (config.PISTE_COLORS).
    # Step 4: Station box: st.info "Snow data from station X (1,594 m, 3 km away)", or st.warning
    #         "No reliable measurement station nearby. A snow forecast is not available for this resort."
    # Step 5: Travel time if known, then st.button("Check the snow for your holiday", type="primary",
    #         disabled=station is None).
    # Done when: it looks like the prototype's resort card for every resort.
    raise NotImplementedError("TODO [NOAH | Task 11]: resort_card")


# ============================================================================ snow check
def snow_check_dates(default: tuple[date, date]) -> tuple[date, date] | None:
    """
    The (slightly larger) date input at the top of the snow check.

    Owner:    Noah (Task 10: user interface and navigation)
    Used by:  pages/explore.py
    Source:   pre-filled from the sidebar dates, or location.default_trip_dates()
    Returns:  (start, end) if two valid dates are picked, otherwise None (with a friendly message)
    """
    # TODO [NOAH | Task 10] Snow check date input
    # Step 1: st.date_input("Holiday dates", key="check_range"), pre-filled with `default`.
    # Step 2: Make it a bit larger with a small CSS rule on .st-key-check_range (see the prototype).
    # Step 3: Only one date picked -> st.info("Please pick an end date too.") and return None.
    # Step 4: Check with location.validate_holiday_range; show st.warning and return None if invalid.
    # Done when: dates in July show "Snow-Proof covers the ski season from December to April".
    raise NotImplementedError("TODO [NOAH | Task 10]: snow_check_dates")


def chance_bar(chance: float, baseline: float) -> None:
    """
    The main result: one bar from 0 to 100% with the chance, and the historical average as a marker.

    Owner:    Noah (Task 11: map, charts and resort details)
    Used by:  pages/explore.py
    Source:   data_access.predict_good_week() -> chance and baseline
    Returns:  nothing
    """
    # TODO [NOAH | Task 11] Chance bar with baseline
    # Step 1: Big text "68% chance of a good ski week" in the traffic light color.
    # Step 2: A bar from 0 to 100% filled up to the chance, with a thin marker at the baseline,
    #         and the text "Historical average for this week: 61%".
    # Step 3: One sentence of explanation, and the definition "A good ski week means at least
    #         50 cm of snow depth on all 7 days at the linked station" (use config.GOOD_SNOW_CM).
    # Hint:   The prototype draws this with a little HTML in st.markdown. A plotly bar works too.
    # Done when: chance and historical average are shown together, without repeating the numbers elsewhere.
    raise NotImplementedError("TODO [NOAH | Task 11]: chance_bar")


def weekly_chart(weekly: pd.DataFrame) -> go.Figure:
    """
    Chance per week when the stay covers several weeks.

    Owner:    Noah (Task 11: map, charts and resort details)
    Used by:  pages/explore.py
    Source:   predict_good_week()["weekly"] (columns label, chance, baseline)
    Returns:  a plotly Figure
    """
    # TODO [NOAH | Task 11] Weekly chart
    # Step 1: go.Figure with a bar per week (chance in %), colored with the traffic light colors.
    # Step 2: Add the baseline per week as markers (fig.add_scatter with mode="markers").
    # Done when: a 3-week stay shows 3 bars.
    raise NotImplementedError("TODO [NOAH | Task 11]: weekly_chart")


def daily_snow_chart(daily: pd.DataFrame) -> go.Figure:
    """
    Expected snow depth per day of the stay, with an uncertainty band and a dashed 50 cm line.

    Owner:    Noah (Task 11: map, charts and resort details)
    Used by:  pages/explore.py
    Source:   predict_good_week()["daily"] (columns date, expected_cm, low_cm, high_cm)
    Returns:  a plotly Figure
    """
    # TODO [NOAH | Task 11] Snow depth chart
    # Step 1: Draw high_cm and low_cm as two invisible lines and fill between them (fill="tonexty").
    # Step 2: Draw expected_cm as a line with markers.
    # Step 3: fig.add_hline(y=config.GOOD_SNOW_CM, line_dash="dash") with the label "50 cm threshold".
    # Done when: the chart looks like the prototype's "Expected snow depth per day".
    raise NotImplementedError("TODO [NOAH | Task 11]: daily_snow_chart")


def history_chart(history: pd.DataFrame, calendar_week: int) -> go.Figure:
    """
    OPTIONAL: share of good weeks per decade for this calendar week (long-term trend).

    Owner:    Noah (Task 11, optional)
    Used by:  pages/explore.py (optional section)
    Source:   data_access.get_historical_good_week_share() (columns decade, share)
    Returns:  a plotly Figure
    """
    # TODO [NOAH | Task 11, optional] Decade chart
    # Step 1: go.Bar with x=decade and y=share in %.
    # Hint:   Removed from the prototype after feedback. Only build it if the team wants it back.
    # Done when: one bar per decade.
    raise NotImplementedError("TODO [NOAH | Task 11, optional]: history_chart")


def model_info_box(info: dict) -> None:
    """
    The "About this forecast" expander at the bottom of the snow check.

    Owner:    Noah (Task 10: user interface and navigation)
    Used by:  pages/explore.py
    Source:   data_access.get_model_info()
    Returns:  nothing
    """
    # TODO [NOAH | Task 10] Model info box
    # Step 1: st.expander("About this forecast") with station, training period and final test scores.
    # Step 2: Add the disclaimer: a station is not the whole resort, slopes can differ,
    #         this is a probability, not a promise.
    # Done when: it matches the prototype's box.
    raise NotImplementedError("TODO [NOAH | Task 10]: model_info_box")


# ============================================================================ model page
def walk_forward_timeline(results: pd.DataFrame) -> go.Figure:
    """
    Training and test periods of each validation round as horizontal bars on a year axis.

    Owner:    Noah + Julian (Task 11 and Task 7)
    Used by:  pages/about_model.py
    Source:   data_access.get_validation_results() (columns round, train_period, test_period)
    Returns:  a plotly Figure
    """
    # TODO [NOAH+JULIAN | Task 11] Walk-forward timeline
    # Step 1: For each round, split "1950-1969" into start and end year.
    # Step 2: Add one horizontal bar for training and one for testing (orientation="h", base=start year).
    # Hint:   barmode="overlay" and yaxis autorange="reversed" put Round 1 on top.
    # Done when: the timeline matches the rounds in snowproof/model.py.
    raise NotImplementedError("TODO [NOAH+JULIAN | Task 11]: walk_forward_timeline")


def model_vs_baseline_chart(results: pd.DataFrame, model_col: str, baseline_col: str, title: str) -> go.Figure:
    """
    Grouped bars: our model versus the historical baseline, per round.

    Owner:    Noah (Task 11: map, charts and resort details)
    Used by:  pages/about_model.py
    Source:   data_access.get_validation_results()
    Returns:  a plotly Figure
    """
    # TODO [NOAH | Task 11] Model versus baseline chart
    # Step 1: Two go.Bar traces (model and baseline) with x=round, barmode="group".
    # Hint:   Call it twice: once for accuracy (higher is better), once for Brier (lower is better).
    # Done when: both charts show 5 rounds with two bars each.
    raise NotImplementedError("TODO [NOAH | Task 11]: model_vs_baseline_chart")
