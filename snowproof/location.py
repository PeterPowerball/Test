"""
location.py: where the user starts, how far the resorts are, school holidays, the filters and the ranking.

Owner:       Jan (Task 8: location, travel and holiday filters, Task 9: resort ranking)
Depends on:  config.py
Used by:     pages/explore.py (sidebar, map, ranked list), data_access.py, pipeline.py step 1
Flow:        Step 1 of 5 (holidays and transport stops), then live in the app

Sections in this file (in the order you build them):
  1. swisstopo         find a city / village, altitudes
  2. Public transport  travel time
  3. School holidays
  4. Filters           canton, travel time, holiday dates (all OPTIONAL for the user)
  5. Ranking           best resorts first

The app only asks for a city or village (no street address), to protect the user's privacy.
"""

from datetime import date

import pandas as pd
import requests

from snowproof import config


# ============================================================================
# swisstopo: find a city / village, altitudes
# ============================================================================

def search_place(query: str) -> dict | None:
    """
    Find a Swiss city or village by name.

    Owner:    Jan (Task 8: location, travel and holiday filters)
    Used by:  data_access.get_travel_time_minutes()
    Source:   swisstopo SearchServer, config.SWISSTOPO_SEARCH_URL
    Returns:  dict with keys label (str, e.g. "Zürich (ZH)"), lat (float), lon (float),
              or None if nothing was found
    """
    # TODO [JAN | Task 8] Search a city or village
    # Step 1: Call the SearchServer with params searchText=query, type="locations",
    #         origins="gg25" (municipalities), sr=4326 (so you get lat/lon), lang="en".
    #         Example: .../SearchServer?searchText=Zurich&type=locations&origins=gg25&sr=4326
    # Step 2: Take the first entry of response.json()["results"].
    # Step 3: Read label, lat and lon from its "attrs".
    # Hint:   The label contains HTML tags like <b>. Remove them before showing it.
    # Hint:   Return None (not an error) for empty input or no results, so the app can show a friendly message.
    # Done when: search_place("Zurich") returns lat about 47.37 and lon about 8.54.
    raise NotImplementedError("TODO [JAN | Task 8]: search_place")


def wgs84_to_lv95(lat: float, lon: float) -> tuple[float, float]:
    """
    Convert lat/lon degrees to Swiss LV95 coordinates (east, north in meters).

    Owner:    Jan (Task 8: location, travel and holiday filters)
    Used by:  get_altitude()
    Source:   swisstopo approximate formulas ("Approximate formulas for the transformation
              between Swiss projection coordinates and WGS84", PDF on swisstopo.admin.ch)
    Returns:  (east, north), e.g. about (2600000, 1200000) near Bern
    """
    # TODO [JAN | Task 8] Convert lat/lon to LV95
    # Step 1: Find the swisstopo PDF with the approximate formulas (search the title above).
    # Step 2: Convert degrees to arc seconds, then to the auxiliary values the PDF describes.
    # Step 3: Apply the polynomial for east and north, and add 2'000'000 / 1'000'000 for LV95.
    # Hint:   Alternative: the geo.admin.ch "reframe" service converts coordinates for you.
    # Done when: wgs84_to_lv95(46.95108, 7.43864) returns about (2600000, 1200000) (Bern).
    raise NotImplementedError("TODO [JAN | Task 8]: wgs84_to_lv95")


def get_altitude(lat: float, lon: float) -> float | None:
    """
    Altitude above sea level for one point.

    Owner:    Jan (Task 8: location, travel and holiday filters), used by Nico for resorts
    Used by:  pipeline.py step 2 (base and summit altitude of resorts), station checks
    Source:   swisstopo height service, config.SWISSTOPO_HEIGHT_URL
    Returns:  altitude in m (float), or None if the point is outside Switzerland
    """
    # TODO [JAN | Task 8] Look up an altitude
    # Step 1: Convert the point with wgs84_to_lv95(lat, lon).
    # Step 2: Call the height service with params easting=..., northing=..., sr=2056.
    # Step 3: Read the "height" value from the JSON and turn it into a float.
    # Hint:   The height service needs LV95 coordinates, not lat/lon. That's why step 1 exists.
    # Done when: get_altitude(46.81, 9.84) returns a value around 1550 (Davos).
    raise NotImplementedError("TODO [JAN | Task 8]: get_altitude")


# ============================================================================
# Public transport: travel time
# ============================================================================

def find_nearest_stop(lat: float, lon: float) -> dict | None:
    """
    The public transport stop closest to a point (e.g. the valley station of a resort).

    Owner:    Jan (Task 8: location, travel and holiday filters)
    Used by:  pipeline.py step 1 -> data.save_table(..., "transport_stops")
    Source:   transport.opendata.ch /v1/locations
    Returns:  dict with keys stop_id (str), stop_name (str), lat (float), lon (float), distance_m (float),
              or None if there is no stop nearby
    """
    # TODO [JAN | Task 8] Find the nearest stop
    # Step 1: Call f"{config.TRANSPORT_BASE_URL}/locations" with params x=lat, y=lon, type="station".
    # Step 2: Take the first station of the result (they come sorted by distance).
    # Hint:   For resorts, run this once in the download script and store the stops in SQLite.
    # Done when: find_nearest_stop(46.02, 7.75) returns a stop in Zermatt.
    raise NotImplementedError("TODO [JAN | Task 8]: find_nearest_stop")


def fetch_travel_time_minutes(from_place: str, to_stop: str, travel_date: date) -> int | None:
    """
    Fastest public transport connection in minutes between a place and a stop.

    Owner:    Jan (Task 8: location, travel and holiday filters)
    Used by:  data_access.get_travel_time_minutes()
    Source:   transport.opendata.ch /v1/connections
    Returns:  travel time in minutes (int), or None if no connection was found
    """
    # TODO [JAN | Task 8] Get the travel time
    # Step 1: Call f"{config.TRANSPORT_BASE_URL}/connections" with params from=from_place, to=to_stop,
    #         date="YYYY-MM-DD", time="08:00", limit=4.
    # Step 2: Each connection has a "duration" like "00d02:35:00". Turn it into minutes.
    # Step 3: Return the shortest duration.
    # Hint:   Dates far in the future can return no connections. Plan a fallback: ask for the
    #         same weekday in the next weeks instead, or use a fixed reference date.
    # Hint:   The API has a rate limit. Cache answers (same city and resort = same answer).
    # Done when: fetch_travel_time_minutes("Zürich HB", "Davos Platz", <a weekday next week>) returns about 140.
    raise NotImplementedError("TODO [JAN | Task 8]: fetch_travel_time_minutes")


# ============================================================================
# School holidays
# ============================================================================

def fetch_school_holidays(valid_from: date, valid_to: date) -> pd.DataFrame:
    """
    School holiday periods of all Swiss cantons between two dates.

    Owner:    Jan (Task 8: location, travel and holiday filters)
    Used by:  pipeline.py step 1 -> data.save_table(..., "holiday_periods")
    Source:   OpenHolidays API /SchoolHolidays, config.OPENHOLIDAYS_URL
    Returns:  DataFrame with columns
                canton (str, e.g. "ZH"), holiday_name (str, e.g. "Sportferien"),
                start_date (datetime.date), end_date (datetime.date)
    """
    # TODO [JAN | Task 8] Download school holidays
    # Step 1: Call f"{config.OPENHOLIDAYS_URL}/SchoolHolidays" with params countryIsoCode="CH",
    #         languageIsoCode="EN", validFrom="YYYY-MM-DD", validTo="YYYY-MM-DD".
    # Step 2: Each entry has "subdivisions" with codes like "CH-ZH". Turn them into canton codes.
    # Step 3: Keep only periods that touch the ski season (config.SEASON_MONTHS).
    # Hint:   Sportferien are often missing or differ by municipality. The user must ALWAYS be able
    #         to pick dates manually. This helper only suggests dates.
    # Hint:   The API allows at most about 3 years per request.
    # Done when: the result has rows for ZH and BE with Christmas holidays.
    raise NotImplementedError("TODO [JAN | Task 8]: fetch_school_holidays")


# ============================================================================
# Filters: canton, travel time, holiday dates
# ============================================================================

def validate_holiday_range(start: date, end: date) -> str | None:
    """
    Check the user's holiday dates.

    Owner:    Jan (Task 8: location, travel and holiday filters)
    Used by:  pages/explore.py (sidebar and snow check), model.predict_good_week()
    Source:   config.SEASON_MONTHS, config.MAX_STAY_DAYS
    Returns:  a friendly error message (str) if the dates are not usable, otherwise None
    """
    # TODO [JAN | Task 8] Validate the holiday dates
    # Step 1: End before start -> return a message.
    # Step 2: Longer than config.MAX_STAY_DAYS -> return a message.
    # Step 3: Any day outside config.SEASON_MONTHS (December to April) -> return
    #         "Snow-Proof covers the ski season from December to April. ..."
    # Step 4: Otherwise return None.
    # Hint:   The prototype's mock_data._validate_holiday_range shows the expected messages.
    #         Write it yourself, then delete the mock copy.
    # Done when: (1 Feb to 7 Feb) gives None, and (1 Jul to 7 Jul) gives a message.
    raise NotImplementedError("TODO [JAN | Task 8]: validate_holiday_range")


def default_trip_dates(today: date) -> tuple[date, date]:
    """
    A sensible default week for the snow check when the user has not set dates yet.

    Owner:    Jan (Task 8: location, travel and holiday filters)
    Used by:  pages/explore.py (pre-fill of the snow check date input)
    Source:   today's date
    Returns:  (start, end) of the next mid-February week, 7 days long
    """
    # TODO [JAN | Task 8] Default trip dates
    # Step 1: Take 13 February of this year. If that is already in the past, use next year.
    # Step 2: end = start + 6 days (datetime.timedelta).
    # Done when: default_trip_dates(date(2026, 10, 22)) returns (2027-02-13, 2027-02-19).
    raise NotImplementedError("TODO [JAN | Task 8]: default_trip_dates")


def filter_by_canton(resorts: pd.DataFrame, cantons: list[str]) -> pd.DataFrame:
    """
    Keep only resorts in the selected cantons (all resorts if the list is empty).

    Owner:    Jan (Task 8: location, travel and holiday filters)
    Used by:  pages/explore.py
    Source:   data_access.get_resorts()
    Returns:  the filtered resorts DataFrame (same columns)
    """
    # TODO [JAN | Task 8] Canton filter
    # Step 1: If cantons is empty, return resorts unchanged.
    # Step 2: Otherwise keep rows whose canton is in the list (pandas Series.isin).
    # Done when: filter_by_canton(resorts, ["VS"]) only returns Valais resorts.
    raise NotImplementedError("TODO [JAN | Task 8]: filter_by_canton")


def filter_by_travel_time(resorts: pd.DataFrame, place: str, max_minutes: float) -> pd.DataFrame:
    """
    Keep only resorts reachable within max_minutes by public transport from the user's city / village.

    Owner:    Jan (Task 8: location, travel and holiday filters)
    Used by:  pages/explore.py
    Source:   data_access.get_travel_time_minutes()
    Returns:  the filtered resorts DataFrame plus a column travel_minutes (int or None)
    """
    # TODO [JAN | Task 8] Travel time filter
    # Step 1: If place is empty, return resorts unchanged (travel_minutes = None).
    # Step 2: Get the travel time for every resort with data_access.get_travel_time_minutes.
    # Step 3: Keep resorts with travel_minutes <= max_minutes.
    # Hint:   If the place is not recognised (all None), don't hide everything. Return all resorts
    #         and let the page show "City / village not recognised".
    # Hint:   Calling the transport API for every resort is slow. Cache (st.cache_data) and keep it simple.
    # Done when: "Geneva" with 60 minutes returns no Grisons resorts.
    raise NotImplementedError("TODO [JAN | Task 8]: filter_by_travel_time")


# ============================================================================
# Ranking: best resorts first
# ============================================================================

def rank_resorts(predictions: pd.DataFrame) -> pd.DataFrame:
    """
    Sort resorts from best to worst chance.

    Owner:    Jan (Task 9: resort ranking)
    Used by:  data_access.get_ranked_resorts()
    Source:   one row per resort with columns resort_id, name, canton, chance, baseline, travel_minutes
    Returns:  the same columns, sorted by chance (best first), resorts without a station removed,
              plus a column rank (int, 1 = best)
    """
    # TODO [JAN | Task 9] Rank resorts
    # Step 1: Drop rows where chance is missing (resorts without a reliable station).
    # Step 2: Sort by chance, highest first (DataFrame.sort_values).
    # Step 3: Add the rank column and reset the index.
    # Hint:   Think about ties: with equal chance, should the shorter travel time win? Decide as a team.
    # Done when: the first row has the highest chance and rank 1.
    raise NotImplementedError("TODO [JAN | Task 9]: rank_resorts")


def find_similar_resorts(resort_id: str, start_date: date, end_date: date,
                         place: str = "", count: int = 3) -> pd.DataFrame:
    """
    OPTIONAL: other resorts with a better chance and a similar travel time.

    Owner:    Jan (Task 9, optional)
    Used by:  pages/explore.py (optional "Similar resorts with better chances" section)
    Source:   data_access.get_ranked_resorts(), data_access.get_travel_time_minutes()
    Returns:  same columns as rank_resorts(), at most `count` rows
    """
    # TODO [JAN | Task 9, optional] Similar resorts with better chances
    # Step 1: Rank all other resorts for the same dates.
    # Step 2: Keep those with a clearly higher chance (e.g. at least 2 points more).
    # Step 3: "Similar": within 60 minutes of this resort's travel time, or within 150 km if no place is set.
    # Hint:   This section was removed from the prototype after feedback. Only build it if the team wants it.
    # Done when: a low resort in December gets higher alternatives nearby.
    raise NotImplementedError("TODO [JAN | Task 9, optional]: find_similar_resorts")
