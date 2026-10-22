"""
transport.py: travel time by public transport (transport.opendata.ch).

Owner:       Jan (Task 8: location, travel and holiday filters)
Depends on:  config.py
Used by:     data_access.get_travel_time_minutes(), scripts/01_download_data.py (resort stops)
Flow:        Step 1 of 5 (resort stops), and live in the app for the travel time filter
"""

from datetime import date

import pandas as pd
import requests

from snowproof import config


def find_nearest_stop(lat: float, lon: float) -> dict | None:
    """
    The public transport stop closest to a point (e.g. the valley station of a resort).

    Owner:    Jan (Task 8: location, travel and holiday filters)
    Used by:  scripts/01_download_data.py -> database.save_table(..., "transport_stops")
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
