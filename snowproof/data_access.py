"""
data_access.py: the ONLY place where the app gets its data from.

Owner:       Fabio (Task 12: integration and testing). Real versions per function as tagged below.
Depends on:  config.py, mock_data.py (while USE_MOCK_DATA is True), data.py, model.py, location.py
Used by:     all pages
Flow:        app. Connects the results of steps 1 to 5 to the user interface.

How it works:
  Every function starts with "if config.USE_MOCK_DATA: return mock_data.<function>(...)".
  So Noah can build the whole UI on mock data today. When the real data and model are ready,
  the owner writes the real version below the mock line, and Fabio switches
  config.USE_MOCK_DATA to False during integration.

Rule: keep the return format (column names, units) EXACTLY as in the docstrings.
Then the pages never need to change.
"""

from datetime import date

import pandas as pd
import streamlit as st

from snowproof import config, data, location, mock_data, model


@st.cache_data
def get_resorts() -> pd.DataFrame:
    """
    All ski resorts, one row each.

    Owner:    Fabio (Task 12), data from Nico (Task 5)
    Source:   resorts and resort_station_mapping tables (filled from OpenStreetMap, swisstopo, MeteoSwiss)
    Returns:  DataFrame with columns
                resort_id, name, canton, lat, lon (degrees), base_altitude_m, summit_altitude_m (m),
                piste_blue_km, piste_red_km, piste_black_km, total_piste_km (km), lifts (count),
                description, station_name, station_altitude_m (m), station_distance_km (km), has_station (bool)
    """
    if config.USE_MOCK_DATA:
        return mock_data.get_resorts()
    # TODO [FABIO | Task 12] Real resorts
    # Step 1: Load the resorts table with data.load_table("resorts").
    # Step 2: Merge resort_station_mapping and stations to add the station columns and has_station.
    # Step 3: Make sure every column of the docstring exists with the same name.
    # Done when: the explore page looks the same as with mock data, but with all real resorts.
    raise NotImplementedError("TODO [FABIO | Task 12]: get_resorts")


@st.cache_data
def get_cantons() -> list[str]:
    """
    Cantons that have at least one resort, sorted (for the canton filter).

    Owner:    Fabio (Task 12)
    Source:   get_resorts()
    Returns:  list of canton codes, e.g. ["BE", "GR", "VS"]
    """
    if config.USE_MOCK_DATA:
        return mock_data.get_cantons()
    # TODO [FABIO | Task 12] Real cantons
    # Step 1: Take the unique values of get_resorts()["canton"] and sort them.
    # Done when: the list has no duplicates and no empty values.
    raise NotImplementedError("TODO [FABIO | Task 12]: get_cantons")


@st.cache_data
def get_school_holiday_cantons() -> list[str]:
    """
    All 26 canton codes (for the school holiday helper).

    Owner:    Jan (Task 8)
    Source:   holiday_periods table
    Returns:  sorted list of canton codes
    """
    if config.USE_MOCK_DATA:
        return mock_data.get_school_holiday_cantons()
    # TODO [JAN | Task 8] Real holiday cantons
    # Step 1: Load holiday_periods and return the sorted unique canton codes.
    # Done when: the list has 26 entries (or explain which are missing).
    raise NotImplementedError("TODO [JAN | Task 8]: get_school_holiday_cantons")


@st.cache_data
def get_resort_details(resort_id: str) -> dict:
    """
    All facts about one resort.

    Owner:    Fabio (Task 12)
    Source:   get_resorts()
    Returns:  dict with the same keys as the get_resorts() columns
    """
    if config.USE_MOCK_DATA:
        return mock_data.get_resort_details(resort_id)
    # TODO [FABIO | Task 12] Real resort details
    # Step 1: Find the row of get_resorts() with this resort_id and return it as a dict (Series.to_dict).
    # Hint:   Raise a KeyError with a clear message for an unknown resort_id.
    # Done when: get_resort_details("davos")["name"] returns the resort's name.
    raise NotImplementedError("TODO [FABIO | Task 12]: get_resort_details")


@st.cache_data
def get_pistes(resort_id: str) -> pd.DataFrame:
    """
    Piste length by difficulty for one resort.

    Owner:    Fabio (Task 12), data from Nico (Task 5)
    Source:   pistes table (length_km from data.compute_piste_km)
    Returns:  DataFrame with columns difficulty ("Blue (easy)", "Red (medium)", "Black (difficult)"), km
    """
    if config.USE_MOCK_DATA:
        return mock_data.get_pistes(resort_id)
    # TODO [FABIO | Task 12] Real piste km per difficulty
    # Step 1: Load the pistes of this resort (data.load_table with where="resort_id = ?").
    # Step 2: Map OSM difficulties to Swiss colors: easy -> Blue, intermediate -> Red, advanced/expert -> Black.
    # Step 3: Sum length_km per color and return the three rows.
    # Done when: the three km values add up to the resort's total_piste_km.
    raise NotImplementedError("TODO [FABIO | Task 12]: get_pistes")


@st.cache_data
def get_linked_station(resort_id: str) -> dict | None:
    """
    The measurement station used for the snow data, or None if there is no reliable one.

    Owner:    Fabio (Task 12), data from Nico (Task 4)
    Source:   resort_station_mapping and stations tables
    Returns:  dict with keys name, altitude_m (m), distance_km (km), or None
    """
    if config.USE_MOCK_DATA:
        return mock_data.get_linked_station(resort_id)
    # TODO [FABIO | Task 12] Real linked station
    # Step 1: Read the mapping row for this resort. If is_reliable is false, return None.
    # Step 2: Otherwise return the station's name, altitude_m and distance_km.
    # Done when: a resort without a reliable station shows the grey dot and the warning box.
    raise NotImplementedError("TODO [FABIO | Task 12]: get_linked_station")


@st.cache_data
def get_travel_time_minutes(place: str, resort_id: str) -> int | None:
    """
    Travel time by public transport from the user's city / village, or None if unknown.

    Owner:    Jan (Task 8)
    Source:   location.search_place(), transport_stops table, location.fetch_travel_time_minutes()
    Returns:  minutes (int) or None
    """
    if config.USE_MOCK_DATA:
        return mock_data.get_travel_time_minutes(place, resort_id)
    # TODO [JAN | Task 8] Real travel time
    # Step 1: Return None for empty input.
    # Step 2: Check the place exists with location.search_place(place) (None -> return None).
    # Step 3: Look up the resort's stop in the transport_stops table.
    # Step 4: Return location.fetch_travel_time_minutes(place label, stop name, a reference date).
    # Hint:   st.cache_data above means the same place and resort are only asked once.
    # Done when: "Zurich" to Davos returns roughly 2 to 2.5 hours.
    raise NotImplementedError("TODO [JAN | Task 8]: get_travel_time_minutes")


@st.cache_data
def get_school_holidays(canton: str) -> list[tuple[date, date]]:
    """
    School holiday periods of a canton for the coming winter.

    Owner:    Jan (Task 8)
    Source:   holiday_periods table (from the OpenHolidays API)
    Returns:  list of (start_date, end_date) pairs
    """
    if config.USE_MOCK_DATA:
        return mock_data.get_school_holidays(canton)
    # TODO [JAN | Task 8] Real school holidays
    # Step 1: Load holiday_periods for this canton (where="canton = ?").
    # Step 2: Keep the coming winter only, return (start_date, end_date) pairs sorted by date.
    # Hint:   An empty list is fine. The user can always pick dates by hand.
    # Done when: "ZH" returns the Zurich Christmas and Sportferien dates.
    raise NotImplementedError("TODO [JAN | Task 8]: get_school_holidays")


@st.cache_data
def predict_good_week(resort_id: str, start_date: date, end_date: date) -> dict:
    """
    Chance of a good ski week for a stay (at least 50 cm on all 7 days at the linked station).

    Owner:    Julian (Task 7)
    Source:   our own ML model (precomputed in the weekly_predictions table by script 05)
    Returns:  dict with keys available, reason, chance, baseline, weekly (DataFrame), daily (DataFrame)
              (exact format: see model.predict_good_week)
    """
    if config.USE_MOCK_DATA:
        return mock_data.predict_good_week(resort_id, start_date, end_date)
    # TODO [JULIAN | Task 7] Real prediction
    # Step 1: return model.predict_good_week(resort_id, start_date, end_date).
    # Done when: the snow check shows real chances.
    raise NotImplementedError("TODO [JULIAN | Task 7]: predict_good_week (data_access)")


@st.cache_data
def get_historical_good_week_share(resort_id: str, calendar_week: int) -> pd.DataFrame:
    """
    OPTIONAL (decade chart): share of good weeks per decade for one calendar week.

    Owner:    Julian (Task 6, optional)
    Source:   weekly_labels via model.share_per_decade()
    Returns:  DataFrame with columns decade (str), share (float, 0 to 1)
    """
    if config.USE_MOCK_DATA:
        return mock_data.get_historical_good_week_share(resort_id, calendar_week)
    # TODO [JULIAN | Task 6, optional] Real decade shares
    # Step 1: Find the resort's station, load weekly_labels for it.
    # Step 2: return model.share_per_decade(labels, station_code, calendar_week).
    # Done when: the optional decade chart shows real decades.
    raise NotImplementedError("TODO [JULIAN | Task 6, optional]: get_historical_good_week_share")


@st.cache_data
def get_validation_results() -> pd.DataFrame:
    """
    Walk-forward validation results, model versus historical baseline.

    Owner:    Julian (Task 7)
    Source:   model_runs table (written by pipeline.py step 4)
    Returns:  DataFrame with columns round, train_period, test_period, model_accuracy,
              baseline_accuracy, model_brier, baseline_brier
    """
    if config.USE_MOCK_DATA:
        return mock_data.get_validation_results()
    # TODO [JULIAN | Task 7] Real validation results
    # Step 1: Load model_runs, keep only the final model's latest run.
    # Step 2: Return the columns above, one row per round (final check last).
    # Done when: the "About our model" page shows our real numbers.
    raise NotImplementedError("TODO [JULIAN | Task 7]: get_validation_results")


@st.cache_data
def get_model_info(resort_id: str) -> dict:
    """
    Short facts for the "About this forecast" box of one resort.

    Owner:    Julian (Task 7)
    Source:   model_runs table and get_linked_station()
    Returns:  dict with keys station (dict or None), training_period (str), final_test_period (str),
              final_accuracy (float), final_brier (float)
    """
    if config.USE_MOCK_DATA:
        return mock_data.get_model_info(resort_id)
    # TODO [JULIAN | Task 7] Real model info
    # Step 1: Take the final check row of get_validation_results().
    # Step 2: Return the dict above, with get_linked_station(resort_id) as station.
    # Done when: the box shows the real training period and final scores.
    raise NotImplementedError("TODO [JULIAN | Task 7]: get_model_info")


@st.cache_data
def get_ranked_resorts(resort_ids: tuple[str, ...], start_date: date, end_date: date,
                       place: str = "") -> pd.DataFrame:
    """
    Resorts ranked by chance of a good week (best first). Resorts without a station are left out.

    Owner:    Jan (Task 9)
    Source:   predict_good_week(), get_travel_time_minutes(), location.rank_resorts()
    Returns:  DataFrame with columns resort_id, name, canton, chance, baseline, travel_minutes
    """
    if config.USE_MOCK_DATA:
        return mock_data.get_ranked_resorts(resort_ids, start_date, end_date, place)
    # TODO [JAN | Task 9] Real ranking
    # Step 1: For each resort_id, call predict_good_week and get_travel_time_minutes.
    # Step 2: Collect one row per resort (skip "available": False) and pass them to location.rank_resorts.
    # Done when: the ranked list below the map shows real resorts in the right order.
    raise NotImplementedError("TODO [JAN | Task 9]: get_ranked_resorts")
