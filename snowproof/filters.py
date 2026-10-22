"""
filters.py: the optional sidebar filters (canton, travel time, holiday dates).

Owner:       Jan (Task 8: location, travel and holiday filters)
Depends on:  config.py
Used by:     pages/explore.py (sidebar and map), data_access.py
Flow:        app (runs live when the user changes a filter)

All filters are OPTIONAL. With no filter set, every resort must still be shown.
"""

from datetime import date

import pandas as pd

from snowproof import config


def validate_holiday_range(start: date, end: date) -> str | None:
    """
    Check the user's holiday dates.

    Owner:    Jan (Task 8: location, travel and holiday filters)
    Used by:  pages/explore.py (sidebar and snow check), ml/predict.py
    Source:   config.SEASON_MONTHS, config.MAX_STAY_DAYS
    Returns:  a friendly error message (str) if the dates are not usable, otherwise None
    """
    # TODO [JAN | Task 8] Validate the holiday dates
    # Step 1: End before start -> return a message.
    # Step 2: Longer than config.MAX_STAY_DAYS -> return a message.
    # Step 3: Any day outside config.SEASON_MONTHS (December to April) -> return
    #         "Snow-Proof covers the ski season from December to April. ..."
    # Step 4: Otherwise return None.
    # Hint:   The prototype's mock_access._validate_holiday_range shows the expected messages.
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
