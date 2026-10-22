"""The ONLY place where the UI gets its data from.

Today every function returns mock data (see mock_data.py). Later, each function can be
replaced one by one with a real source, without touching any page. The docstring of
each function says what it returns and which real source will replace the mock.

Rule for teammates: keep the return format (column names, units) the same when you
swap in the real source, and the UI keeps working.
"""

from datetime import date

import pandas as pd
import streamlit as st

from snowproof import config, mock_data


def _resort_row(resort_id: str) -> pd.Series:
    """Internal helper: one row of the resorts table."""
    table = mock_data.resorts_table()
    match = table[table["resort_id"] == resort_id]
    if match.empty:
        raise KeyError(f"Unknown resort: {resort_id}")
    return match.iloc[0]


@st.cache_data
def get_resorts() -> pd.DataFrame:
    """All ski resorts, one row each.

    Columns: resort_id, name, canton, lat, lon (degrees), base_altitude_m, summit_altitude_m (m),
    piste_blue_km, piste_red_km, piste_black_km, total_piste_km (km), lifts (count),
    description, station_name, station_altitude_m (m), station_distance_km (km), has_station (bool).

    FUTURE SOURCE: OpenStreetMap Overpass API (resorts, pistes, lifts), altitudes from
    swisstopo / api3.geo.admin.ch, station link from MeteoSwiss Open Data.
    """
    return mock_data.resorts_table()


@st.cache_data
def get_cantons() -> list[str]:
    """Cantons that have at least one resort (for the filter), sorted.

    FUTURE SOURCE: derived from get_resorts(), so it follows the OpenStreetMap data.
    """
    return sorted(get_resorts()["canton"].unique().tolist())


@st.cache_data
def get_school_holiday_cantons() -> list[str]:
    """All 26 canton codes, for the school holiday helper.

    FUTURE SOURCE: OpenHolidays API.
    """
    return mock_data.cantons()


@st.cache_data
def get_resort_details(resort_id: str) -> dict:
    """All facts about one resort as a dict (same keys as the get_resorts() columns).

    FUTURE SOURCE: OpenStreetMap Overpass API, swisstopo / api3.geo.admin.ch (altitudes).
    """
    return _resort_row(resort_id).to_dict()


@st.cache_data
def get_pistes(resort_id: str) -> pd.DataFrame:
    """Piste length by difficulty.

    Columns: difficulty ("Blue (easy)", "Red (medium)", "Black (difficult)"), km (km).

    FUTURE SOURCE: OpenStreetMap Overpass API (piece:type=downhill with piste:difficulty).
    """
    row = _resort_row(resort_id)
    return pd.DataFrame({
        "difficulty": ["Blue (easy)", "Red (medium)", "Black (difficult)"],
        "km": [row["piste_blue_km"], row["piste_red_km"], row["piste_black_km"]],
    })


@st.cache_data
def get_linked_station(resort_id: str) -> dict | None:
    """The measurement station used for the snow data, or None if there is no reliable one.

    Keys: name, altitude_m (m), distance_km (km).

    FUTURE SOURCE: MeteoSwiss Open Data (station list with snow depth measurements),
    matched to the resort by distance and altitude.
    """
    row = _resort_row(resort_id)
    if not row["has_station"]:
        return None
    return {"name": row["station_name"], "altitude_m": int(row["station_altitude_m"]),
            "distance_km": float(row["station_distance_km"])}


@st.cache_data
def get_travel_time_minutes(home_address: str, resort_id: str) -> int | None:
    """Travel time by public transport in minutes, or None if the address is unknown or empty.

    FUTURE SOURCE: swisstopo / api3.geo.admin.ch (geocoding of the address) and
    transport.opendata.ch (public transport connections).
    """
    if not home_address or not home_address.strip():
        return None
    row = _resort_row(resort_id)
    return mock_data.travel_minutes(home_address, row["lat"], row["lon"])


@st.cache_data
def get_school_holidays(canton: str) -> list[tuple[date, date]]:
    """School holiday periods of a canton as (start, end) pairs, for the coming winter.

    FUTURE SOURCE: OpenHolidays API. Note that Sportferien can differ by municipality.
    """
    return mock_data.school_holidays(canton)


@st.cache_data
def predict_good_week(resort_id: str, start_date: date, end_date: date) -> dict:
    """Chance of a good ski week for a stay.

    A good week means at least 50 cm of snow depth on all 7 days at the linked station.
    Returns a dict with:
      available (bool), reason (str, only if not available),
      chance (0 to 1, mean over the weeks of the stay),
      baseline (0 to 1, simple historical average for the same weeks),
      weekly (DataFrame: label, week_start, week_end, chance, baseline),
      daily (DataFrame: date, expected_cm, low_cm, high_cm; snow depth in cm).

    FUTURE SOURCE: our own trained ML model (inputs: MeteoSwiss snow history and
    Open-Meteo Historical / ERA5 weather features).
    """
    row = _resort_row(resort_id)
    if not row["has_station"]:
        return {"available": False, "reason": "No reliable measurement station nearby."}
    problem = config.validate_holiday_range(start_date, end_date)
    if problem:
        return {"available": False, "reason": problem}

    factor = mock_data.resort_factor(resort_id)
    altitude = mock_data.snow_altitude(row)
    weeks = mock_data.split_into_weeks(start_date, end_date)
    weekly_rows = []
    for days in weeks:
        calendar_week = days[0].isocalendar().week
        history = get_historical_good_week_share(resort_id, calendar_week)
        weekly_rows.append({
            "label": f"{days[0]:%d %b} to {days[-1]:%d %b}",
            "week_start": days[0], "week_end": days[-1],
            "chance": mock_data.week_chance(altitude, days, factor),
            "baseline": float(history["share"].mean()),
        })
    weekly = pd.DataFrame(weekly_rows)
    all_days = [d for days in weeks for d in days]
    return {
        "available": True,
        "chance": float(weekly["chance"].mean()),
        "baseline": float(weekly["baseline"].mean()),
        "weekly": weekly,
        "daily": mock_data.daily_forecast(row, all_days),
    }


@st.cache_data
def get_historical_good_week_share(resort_id: str, calendar_week: int) -> pd.DataFrame:
    """Share of good weeks for one ISO calendar week, per decade.

    Columns: decade (e.g. "1950s"), share (0 to 1).

    FUTURE SOURCE: MeteoSwiss Open Data (measured snow depth at the linked station).
    """
    row = _resort_row(resort_id)
    decades = range(1950, 2030, 10)
    return pd.DataFrame({
        "decade": [f"{d}s" for d in decades],
        "share": [mock_data.historical_share(row, calendar_week, d) for d in decades],
    })


@st.cache_data
def get_validation_results() -> pd.DataFrame:
    """Walk-forward validation results of the model versus the simple historical baseline.

    Columns: round, train_period, test_period, model_accuracy, baseline_accuracy
    (share of correct yes/no calls, higher is better), model_brier, baseline_brier
    (probability error, lower is better).

    FUTURE SOURCE: our own trained ML model (output of the validation script).
    """
    return mock_data.validation_table()


@st.cache_data
def get_model_info(resort_id: str) -> dict:
    """Short facts for the model info box of one resort.

    Keys: station (dict or None), training_period (str), final_test_period (str),
    final_accuracy, final_brier (floats, from the final check).

    FUTURE SOURCE: our own trained ML model (metadata and final validation scores).
    """
    final = get_validation_results().iloc[-1]
    return {
        "station": get_linked_station(resort_id),
        "training_period": final["train_period"],
        "final_test_period": final["test_period"],
        "final_accuracy": float(final["model_accuracy"]),
        "final_brier": float(final["model_brier"]),
    }


@st.cache_data
def get_ranked_resorts(resort_ids: tuple[str, ...], start_date: date, end_date: date,
                       home_address: str = "") -> pd.DataFrame:
    """Resorts ranked by chance of a good week (best first). Resorts without a station are left out.

    Columns: resort_id, name, canton, chance (0 to 1), baseline (0 to 1), travel_minutes (min or None).

    FUTURE SOURCE: predictions from our own ML model, travel time from transport.opendata.ch.
    """
    rows = []
    for rid in resort_ids:
        result = predict_good_week(rid, start_date, end_date)
        if not result["available"]:
            continue
        details = get_resort_details(rid)
        rows.append({
            "resort_id": rid, "name": details["name"], "canton": details["canton"],
            "chance": result["chance"], "baseline": result["baseline"],
            "travel_minutes": get_travel_time_minutes(home_address, rid),
        })
    columns = ["resort_id", "name", "canton", "chance", "baseline", "travel_minutes"]
    table = pd.DataFrame(rows, columns=columns)
    return table.sort_values("chance", ascending=False).reset_index(drop=True)
