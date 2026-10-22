"""
explore.py: the main page. Sidebar filters, map, resort card, ranked list and the snow check.

Owner:       Noah (Task 10 and 11), with Jan (Task 8 and 9) for filters and ranking
Depends on:  data_access.py, filters.py, ui_components.py, config.py
Used by:     streamlit_app.py (navigation)
Flow:        app. The user flow from top to bottom:
             filters -> map -> click a resort -> resort card -> "Check the snow" -> snow check

How this skeleton works:
  Every section is wrapped in "try ... except NotImplementedError". As long as a function
  still raises NotImplementedError, the page shows a 🚧 box instead. When you finish your
  function, the box disappears by itself. Do not remove the try/except, it keeps the app running.

Session state keys (agree on these names as a team):
  selected_resort_id  the clicked resort (or None)
  view                "resort" (map and card) or "snow" (snow check)
  last_map_click      the last map click already handled, so old clicks are not replayed
  holiday_range       sidebar dates
  check_range         snow check dates
"""

from datetime import date

import streamlit as st

from snowproof import config, data_access, filters
from snowproof import ui_components as ui

# Skeleton preview: show EVERY section (with a sample resort and sample dates), even before the
# map click and the button work, so everyone sees the whole flow. Noah sets this to False once
# clicking the map and the "Check the snow" button work.
SKELETON_PREVIEW = True
SAMPLE_RESORT_ID = "davos"
SAMPLE_DATES = (date(2027, 2, 13), date(2027, 2, 19))


def init_state() -> None:
    """
    Create the session state keys with their start values (see the list at the top of this file).

    Owner:    Noah (Task 10: user interface and navigation)
    Used by:  this page, once at the top
    Returns:  nothing
    """
    # TODO [NOAH | Task 10] Session state
    # Step 1: st.session_state.setdefault("selected_resort_id", None), same for view ("resort"),
    #         last_map_click (None) and holiday_range (an empty tuple).
    # Hint:   Session state survives reruns. Normal variables are reset on every click.
    # Done when: printing st.session_state shows all keys after the first load.
    raise NotImplementedError("TODO [NOAH | Task 10]: init_state")


def handle_map_click(clicked_name: str | None, resorts) -> None:
    """
    Turn a NEW click on the map into the selected resort.

    Owner:    Noah (Task 11: map, charts and resort details)
    Used by:  this page, right after ui.show_map()
    Source:   the clicked tooltip name from ui.show_map(), resorts from data_access.get_resorts()
    Returns:  nothing (updates st.session_state)
    """
    # TODO [NOAH | Task 11] React to map clicks
    # Step 1: If clicked_name is None or equals st.session_state.last_map_click, do nothing.
    # Step 2: Otherwise store it in last_map_click, find the resort_id with that name, and set
    #         st.session_state.selected_resort_id and view = "resort".
    # Done when: clicking two different dots one after the other switches the resort card.
    raise NotImplementedError("TODO [NOAH | Task 11]: handle_map_click")


# ============================================================================ header
st.title("🏔️ Snow-Proof")
st.markdown("##### Where will the snow be good for your ski holiday?")
st.info("Click your favorite ski destination on the map to see its slopes and check the snow "
        "for your holiday. Use the filters on the left to narrow down the list.", icon="👆")
if config.USE_MOCK_DATA:
    st.caption("Prototype: all numbers are mock data.")

try:
    init_state()
except NotImplementedError:
    ui.todo_box("Session state", "Noah", "Task 10",
                "Create the session state keys listed at the top of pages/explore.py.")

resorts = data_access.get_resorts()

# ============================================================================ sidebar filters
try:
    active = ui.sidebar_filters(data_access.get_cantons(), data_access.get_school_holiday_cantons())
except NotImplementedError:
    with st.sidebar:
        st.header("Filters")
        ui.todo_box("Sidebar filters", "Noah + Jan", "Task 10 and 8",
                    "City / village, canton, max. travel time, holiday dates and the school holiday helper. "
                    "All optional.", preview={"cantons": data_access.get_cantons()})
    active = {"place": "", "cantons": [], "max_minutes": config.MAX_TRAVEL_HOURS * 60, "dates": None}

# ============================================================================ apply the filters
try:
    matching = filters.filter_by_canton(resorts, active["cantons"])
    matching = filters.filter_by_travel_time(matching, active["place"], active["max_minutes"])
    st.markdown(f"**{len(matching)} of {len(resorts)} resorts match**")
except NotImplementedError:
    ui.todo_box("Filter logic", "Jan", "Task 8",
                "Apply the canton and travel time filters and show '14 of 23 resorts match'. "
                "If nothing matches, show a friendly message.")
    matching = resorts

dates = active["dates"] or (SAMPLE_DATES if SKELETON_PREVIEW else None)
ranked, chances = None, None
if active["dates"]:
    ranked = data_access.get_ranked_resorts(tuple(matching["resort_id"]), *active["dates"], active["place"])
    chances = dict(zip(ranked["resort_id"], ranked["chance"]))

# ============================================================================ map
try:
    fmap = ui.build_map(matching, chances)
    clicked = ui.show_map(fmap, key="map")
    handle_map_click(clicked, resorts)
    ui.map_legend(chances is not None)
except NotImplementedError:
    ui.todo_box("Map of Switzerland", "Noah", "Task 11",
                "Full-width folium map with swisstopo tiles. One circle per resort (size = piste km, "
                "grey = no station, traffic light colors when dates are set). Clicking a dot selects the resort.",
                preview=matching[["resort_id", "name", "canton", "lat", "lon", "total_piste_km", "has_station"]])

selected = st.session_state.get("selected_resort_id") or (SAMPLE_RESORT_ID if SKELETON_PREVIEW else None)
view = st.session_state.get("view", "resort")

# ============================================================================ resort card (below the map)
if selected and (view == "resort" or SKELETON_PREVIEW):
    st.subheader("Resort details (appear below the map after a click)")
    try:
        details = data_access.get_resort_details(selected)
        station = data_access.get_linked_station(selected)
        travel = data_access.get_travel_time_minutes(active["place"], selected)
        if ui.resort_card(details, data_access.get_pistes(selected), station, travel):
            st.session_state.view = "snow"
            st.rerun()
    except NotImplementedError:
        ui.todo_box("Resort card", "Noah", "Task 11",
                    "Name, description, piste km, lifts, base and summit altitude, piste km by difficulty, "
                    "linked station (or warning), travel time and the button 'Check the snow for your holiday'.",
                    preview=data_access.get_resort_details(selected))

# ============================================================================ ranked list
if active["dates"] or SKELETON_PREVIEW:
    preview_ranked = ranked if ranked is not None else data_access.get_ranked_resorts(
        tuple(matching["resort_id"]), *SAMPLE_DATES, "")
    try:
        ui.ranked_list(preview_ranked)
    except NotImplementedError:
        ui.todo_box("Ranked resort list", "Noah + Jan", "Task 10 and 9",
                    "Only when holiday dates are set: resorts sorted by chance of a good week, "
                    "with a 'Select' button per row.", preview=preview_ranked.head(10))

# ============================================================================ snow check view
if selected and (view == "snow" or SKELETON_PREVIEW):
    st.divider()
    st.header("Snow check (opens after 'Check the snow for your holiday')")
    st.caption("Needs a 'Back to resort' button at the top that sets st.session_state.view = 'resort'.")

    # 1. Date input
    try:
        check_dates = ui.snow_check_dates(dates or SAMPLE_DATES)
    except NotImplementedError:
        ui.todo_box("Snow check dates", "Noah", "Task 10",
                    "Slightly larger date range input, pre-filled from the sidebar. Only December to April.")
        check_dates = SAMPLE_DATES if SKELETON_PREVIEW else None

    result = data_access.predict_good_week(selected, *check_dates) if check_dates else None

    if result and result["available"]:
        # 2. Main result: chance and historical average together
        try:
            ui.chance_bar(result["chance"], result["baseline"])
        except NotImplementedError:
            ui.todo_box("Chance of a good ski week", "Noah", "Task 11",
                        "One 0 to 100% bar with the chance, a marker for the historical average, "
                        "one sentence of explanation and the 50 cm definition.",
                        preview={"chance": result["chance"], "baseline": result["baseline"]})

        # 3. Charts
        try:
            if len(result["weekly"]) > 1 or SKELETON_PREVIEW:
                st.plotly_chart(ui.weekly_chart(result["weekly"]), width="stretch")
        except NotImplementedError:
            ui.todo_box("Chance per week", "Noah", "Task 11",
                        "Only for stays longer than one week: a bar per week.", preview=result["weekly"])
        try:
            st.plotly_chart(ui.daily_snow_chart(result["daily"]), width="stretch")
        except NotImplementedError:
            ui.todo_box("Expected snow depth per day", "Noah", "Task 11",
                        "Line with uncertainty band and a dashed 50 cm line.", preview=result["daily"])

        # 4. Optional sections (removed from the prototype after feedback, build only if wanted)
        with st.expander("Optional sections (only if the team wants them back)"):
            calendar_week = check_dates[0].isocalendar().week
            try:
                history = data_access.get_historical_good_week_share(selected, calendar_week)
                st.plotly_chart(ui.history_chart(history, calendar_week), width="stretch")
            except NotImplementedError:
                ui.todo_box("Good weeks per decade (optional)", "Noah + Julian", "Task 11 and 6",
                            "Long-term trend for this calendar week.")
            ui.todo_box("Similar resorts with better chances (optional)", "Jan + Noah", "Task 9",
                        "Use ranking.find_similar_resorts and show 3 cards with a 'Check this resort' button.")

        # 5. Model info
        try:
            ui.model_info_box(data_access.get_model_info(selected))
        except NotImplementedError:
            ui.todo_box("About this forecast", "Noah", "Task 10",
                        "Station, training period, final test score, and the disclaimer.",
                        preview=data_access.get_model_info(selected))
    elif result:
        st.warning(result["reason"])
