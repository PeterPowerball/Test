"""Page 1: Explore. Sidebar filters, map, resort panel and the snow check.

Session state keys used here:
  selected_resort_id  the resort the user clicked (or None)
  view                "resort" (map + panel) or "snow" (snow check)
  last_map_click      last tooltip we already handled, so old clicks are not replayed
  map_version         bumped when the selection changes outside the map, to reset the map widget
  holiday_range       sidebar date range
  check_range         date range inside the snow check
"""

from datetime import date

import streamlit as st

from snowproof import config, data_access
from snowproof import ui_components as ui


# --------------------------------------------------------------- state and callbacks
def init_state() -> None:
    st.session_state.setdefault("selected_resort_id", None)
    st.session_state.setdefault("view", "resort")
    st.session_state.setdefault("last_map_click", None)
    st.session_state.setdefault("map_version", 0)
    st.session_state.setdefault("holiday_range", ())


def select_resort(resort_id: str) -> None:
    """Select a resort from outside the map (the ranked list)."""
    st.session_state.selected_resort_id = resort_id
    st.session_state.last_map_click = None  # the new map widget starts without a click
    st.session_state.map_version += 1


def close_resort() -> None:
    """Deselect the resort and hide the details below the map."""
    st.session_state.selected_resort_id = None
    st.session_state.last_map_click = None
    st.session_state.map_version += 1


def use_holidays(start: date, end: date) -> None:
    st.session_state.holiday_range = (start, end)


def open_snow_check(default_range: tuple[date, date] | None) -> None:
    st.session_state.view = "snow"
    st.session_state.check_range = default_range or config.default_trip_dates()


def back_to_resort() -> None:
    st.session_state.view = "resort"


# ------------------------------------------------------------------------- sidebar
def read_holiday_range() -> tuple[date, date] | None:
    """Return the sidebar dates if complete and valid, else None (with a friendly message)."""
    value = st.session_state.get("holiday_range")
    if not isinstance(value, (tuple, list)) or len(value) != 2:
        return None
    problem = config.validate_holiday_range(value[0], value[1])
    if problem:
        st.sidebar.warning(problem)
        return None
    return value[0], value[1]


def render_sidebar() -> dict:
    """Draw the optional filters and return their values."""
    with st.sidebar:
        st.header("Filters")
        st.caption("All optional. You can use the map without them.")
        home = st.text_input("City / village", key="home_address", placeholder="e.g. Zurich",
                             help="Where you start your trip. No street address needed. "
                                  "Prototype: only major Swiss cities are recognised.")
        cantons = st.multiselect("Canton", data_access.get_cantons(), key="cantons")
        max_hours = st.slider("Max. travel time by public transport (hours)", 1.0,
                              config.MAX_TRAVEL_HOURS, config.MAX_TRAVEL_HOURS, 0.5, key="max_hours",
                              disabled=not home.strip())

        with st.expander("Use school holidays of a canton"):
            all_cantons = data_access.get_school_holiday_cantons()
            default = all_cantons.index(cantons[0]) if len(cantons) == 1 else None
            holiday_canton = st.selectbox("Your canton", all_cantons, index=default,
                                          placeholder="Choose a canton", key="holiday_canton")
            if holiday_canton:
                periods = data_access.get_school_holidays(holiday_canton)
                for i, (start, end) in enumerate(periods):
                    st.button(f"{start:%d %b} to {end:%d %b %Y}", key=f"holiday_{i}",
                              on_click=use_holidays, args=(start, end), width="stretch")
            st.caption("Sportferien can differ by municipality. Please double check the dates.")

        st.date_input("Holiday dates", key="holiday_range", format="DD.MM.YYYY",
                      help="Optional. Resorts are then colored by their chance of a good ski week.")
        dates = read_holiday_range()
    return {"home": home.strip(), "cantons": cantons, "max_minutes": max_hours * 60, "dates": dates}


def filter_resorts(resorts, filters: dict):
    """Keep only resorts matching canton and travel time filters."""
    keep = resorts
    if filters["cantons"]:
        keep = keep[keep["canton"].isin(filters["cantons"])]
    if filters["home"]:
        times = {rid: data_access.get_travel_time_minutes(filters["home"], rid) for rid in keep["resort_id"]}
        if any(t is not None for t in times.values()):
            keep = keep[[times[rid] is not None and times[rid] <= filters["max_minutes"]
                         for rid in keep["resort_id"]]]
        else:
            st.sidebar.warning("City / village not recognised. Try a Swiss city such as Zurich or Bern.")
    return keep


# ------------------------------------------------------------------- explore view
def handle_map_click(resorts) -> None:
    """Turn a click on the map into a selection (only if it is a new click)."""
    clicked = st.session_state.get("_clicked_name")
    if clicked and clicked != st.session_state.last_map_click:
        st.session_state.last_map_click = clicked
        match = resorts[resorts["name"] == clicked]
        if not match.empty:
            st.session_state.selected_resort_id = match.iloc[0]["resort_id"]


def render_ranking(matching, filters: dict) -> None:
    """Ranked list of resorts by chance of a good week (needs holiday dates)."""
    start, end = filters["dates"]
    ranked = data_access.get_ranked_resorts(tuple(matching["resort_id"]), start, end, filters["home"])
    st.subheader("Best resorts for your dates")
    if ranked.empty:
        st.info("No resort with snow data matches your filters.")
        return
    for _, r in ranked.head(10).iterrows():
        cols = st.columns([3, 1, 2, 2, 2])
        cols[0].markdown(f"**{r['name']}**")
        cols[1].write(r["canton"])
        cols[2].markdown(f"<b style='color:{config.chance_color(r['chance'])}'>{r['chance']:.0%}</b> chance",
                         unsafe_allow_html=True)
        cols[3].write(ui.format_minutes(r["travel_minutes"]) if r["travel_minutes"] is not None else "-")
        cols[4].button("Select", key=f"rank_{r['resort_id']}", on_click=select_resort, args=(r["resort_id"],))


def render_resort_panel(filters: dict) -> None:
    """Details of the selected resort, shown below the map in two columns."""
    rid = st.session_state.selected_resort_id
    details = data_access.get_resort_details(rid)
    station = data_access.get_linked_station(rid)

    with st.container(border=True):
        title_col, close_col = st.columns([5, 1], vertical_alignment="center")
        title_col.subheader(f"{details['name']} ({details['canton']})")
        close_col.button("Close", on_click=close_resort, width="stretch")

        left, right = st.columns(2, gap="large")
        with left:
            st.write(details["description"])
            m1, m2 = st.columns(2)
            m1.metric("Piste km", f"{details['total_piste_km']:.0f}")
            m2.metric("Lifts", f"{details['lifts']}")
            m1.metric("Base", f"{details['base_altitude_m']:,} m")
            m2.metric("Summit", f"{details['summit_altitude_m']:,} m")
            if filters["home"]:
                minutes = data_access.get_travel_time_minutes(filters["home"], rid)
                if minutes is None:
                    st.caption("Travel time: city / village not recognised.")
                else:
                    st.markdown(f"**Travel time from {filters['home']}:** about "
                                f"{ui.format_minutes(minutes)} by public transport")
        with right:
            ui.show_chart(ui.piste_bar(data_access.get_pistes(rid)))
            ui.station_box(station)

        st.button("Check the snow for your holiday", type="primary", disabled=station is None,
                  on_click=open_snow_check, args=(filters["dates"],), width="stretch")
        if station is None:
            st.caption("Not available: this resort has no reliable measurement station nearby.")


def render_explore(filters: dict) -> None:
    resorts = data_access.get_resorts()
    matching = filter_resorts(resorts, filters)
    st.info("Click your favorite ski destination on the map to see its slopes and check the snow "
            "for your holiday. Use the filters on the left to narrow down the list.", icon="👆")
    st.markdown(f"**{len(matching)} of {len(resorts)} resorts match**")

    chances = None
    if filters["dates"] and not matching.empty:
        start, end = filters["dates"]
        ranked = data_access.get_ranked_resorts(tuple(matching["resort_id"]), start, end, filters["home"])
        chances = dict(zip(ranked["resort_id"], ranked["chance"]))

    # The map always uses the full width, the details appear below it
    fmap = ui.build_map(matching, chances)
    st.session_state["_clicked_name"] = ui.show_map(fmap, key=f"map_{st.session_state.map_version}")
    handle_map_click(resorts)
    ui.map_legend(chances is not None)
    if matching.empty:
        st.info("No resort matches your filters. Try a larger travel time or another canton.")

    if st.session_state.selected_resort_id is not None:
        render_resort_panel(filters)
    if filters["dates"]:
        render_ranking(matching, filters)


# --------------------------------------------------------------------- snow check
def snow_verdict(chance: float, baseline: float) -> str:
    """One friendly sentence explaining the result."""
    diff = round((chance - baseline) * 100)
    comparison = (f"{abs(diff)} points {'above' if diff >= 0 else 'below'} the historical average"
                  if diff else "in line with the historical average")
    if chance >= config.GOOD_CHANCE_MIN:
        return f"Snow looks reliable for these dates, {comparison}."
    if chance >= config.OK_CHANCE_MIN:
        return f"It could go either way, {comparison}. Consider a backup plan."
    return f"Snow is unlikely to be good for these dates, {comparison}."


def render_snow_check(filters: dict) -> None:
    rid = st.session_state.selected_resort_id
    details = data_access.get_resort_details(rid)
    st.button("Back to resort", on_click=back_to_resort)
    st.header(f"Snow check: {details['name']}")

    # Slightly larger date picker: it is the main input of this view
    st.markdown(
        "<style>.st-key-check_range label p {font-size:1.15rem;font-weight:600}"
        ".st-key-check_range input {font-size:1.1rem;min-height:2.8rem}</style>",
        unsafe_allow_html=True,
    )
    st.session_state.setdefault("check_range", config.default_trip_dates())
    st.date_input("Holiday dates", key="check_range", format="DD.MM.YYYY", width=360)
    value = st.session_state.check_range
    if not isinstance(value, (tuple, list)) or len(value) != 2:
        st.info("Please pick an end date too.")
        return
    start, end = value
    problem = config.validate_holiday_range(start, end)
    if problem:
        st.warning(problem)
        return

    result = data_access.predict_good_week(rid, start, end)
    if not result["available"]:
        st.warning(result["reason"])
        return

    # Chance and historical average together in one bar
    ui.chance_bar(result["chance"], result["baseline"], snow_verdict(result["chance"], result["baseline"]))

    # The expected snow depth is what the chance is derived from
    if len(result["weekly"]) > 1:
        c1, c2 = st.columns([3, 2], gap="large")
        with c1:
            ui.show_chart(ui.daily_snow_chart(result["daily"]))
        with c2:
            ui.show_chart(ui.weekly_chart(result["weekly"]))
    else:
        ui.show_chart(ui.daily_snow_chart(result["daily"]))

    info = data_access.get_model_info(rid)
    with st.expander("About this forecast"):
        station = info["station"]
        st.markdown(
            f"- **Station:** {station['name']} ({station['altitude_m']:,} m)\n"
            f"- **Training period:** {info['training_period']}\n"
            f"- **Final test ({info['final_test_period']}), mock:** "
            f"{info['final_accuracy']:.0%} accuracy, Brier score {info['final_brier']:.3f}"
        )
        st.caption("A station is not the whole resort. Conditions on the slopes can differ, "
                   "especially at higher or shadier spots. This is a probability, not a promise.")


# ------------------------------------------------------------------------- page
init_state()
ui.app_header()
active_filters = render_sidebar()
if st.session_state.view == "snow" and st.session_state.selected_resort_id:
    render_snow_check(active_filters)
else:
    render_explore(active_filters)
