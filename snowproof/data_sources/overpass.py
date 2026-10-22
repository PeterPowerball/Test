"""
overpass.py: download ski resorts, pistes and lifts from OpenStreetMap (Overpass API).

Owner:       Nico (Task 5: ski resort information)
Depends on:  config.py
Used by:     scripts/01_download_data.py
Flow:        Step 1 of 5 (download data)

Attribution: data © OpenStreetMap contributors (config.OSM_ATTRIBUTION). Show it in the app.
Why the Swiss instance (config.OVERPASS_URL)? overpass-api.de hung in our tests.
Cache the results in SQLite (see database.fetch_with_cache): Overpass is slow and shared by everyone.
"""

import pandas as pd
import requests

from snowproof import config


def run_overpass_query(query: str) -> dict:
    """
    Send one Overpass QL query and return the JSON answer.

    Owner:    Nico (Task 5: ski resort information)
    Used by:  fetch_ski_areas(), fetch_pistes(), fetch_lifts()
    Source:   config.OVERPASS_URL
    Returns:  dict, the parsed JSON (the objects are in result["elements"])
    """
    # TODO [NICO | Task 5] Send a query to Overpass
    # Step 1: POST the query as form data: requests.post(config.OVERPASS_URL, data={"data": query}, ...).
    # Step 2: Check response.status_code. 429 or 504 means "too busy": wait and try again later.
    # Step 3: Return response.json().
    # Hint:   Start every query with [out:json][timeout:180]; so you get JSON and enough time.
    # Hint:   Try your queries first on https://overpass-turbo.eu to see what comes back.
    # Done when: run_overpass_query('[out:json];node["name"="Davos"];out;') returns a dict with "elements".
    raise NotImplementedError("TODO [NICO | Task 5]: run_overpass_query")


def fetch_ski_areas() -> pd.DataFrame:
    """
    All ski resorts (winter sports areas) in Switzerland.

    Owner:    Nico (Task 5: ski resort information)
    Used by:  scripts/01_download_data.py -> database.save_table(..., "resorts")
    Source:   OpenStreetMap via Overpass
    Returns:  DataFrame with columns
                resort_id (str, short and stable, e.g. "davos"), osm_id (int), name (str),
                lat (float), lon (float), canton (str, filled later in preparation)
    """
    # TODO [NICO | Task 5] Download all Swiss ski areas
    # Step 1: Write a query for areas inside Switzerland, e.g. area["ISO3166-1"="CH"]->.ch;
    #         then landuse=winter_sports objects inside that area.
    # Step 2: Use "out center;" so you get one point (center) per area.
    # Step 3: Build the table. Make resort_id from the name (lowercase, no spaces or umlauts).
    # Hint:   Some resorts have no name or are tiny (one rope tow). Drop those, or keep a minimum size.
    # Hint:   Big regions (e.g. "4 Vallées") can appear as several areas. Decide as a team how to merge.
    # Done when: the table has at least 100 rows and contains Zermatt, Davos and Laax.
    raise NotImplementedError("TODO [NICO | Task 5]: fetch_ski_areas")


def fetch_pistes() -> pd.DataFrame:
    """
    All downhill pistes in Switzerland with their full line geometry.

    Owner:    Nico (Task 5: ski resort information)
    Used by:  scripts/01_download_data.py, then compute_piste_km()
    Source:   OpenStreetMap via Overpass (piste:type=downhill)
    Returns:  DataFrame with columns
                osm_id (int), difficulty (str: "easy", "intermediate", "advanced", "expert" or None),
                coordinates (list of (lat, lon) tuples along the line)
    """
    # TODO [NICO | Task 5] Download all downhill pistes
    # Step 1: Query ways with "piste:type"="downhill" inside Switzerland.
    # Step 2: Use "out geom;" so every way comes with its full list of points (not just node ids).
    # Step 3: Read "piste:difficulty" from the tags of each element.
    # Hint:   Piste km must be calculated from the line geometry (compute_piste_km), not by counting objects.
    # Hint:   This query is big. Run it once and cache it (database.fetch_with_cache).
    # Done when: the table has thousands of rows and every row has at least 2 coordinates.
    raise NotImplementedError("TODO [NICO | Task 5]: fetch_pistes")


def fetch_lifts() -> pd.DataFrame:
    """
    All ski lifts (aerialways) in Switzerland.

    Owner:    Nico (Task 5: ski resort information)
    Used by:  scripts/01_download_data.py, then preparation (count lifts per resort)
    Source:   OpenStreetMap via Overpass (aerialway=*)
    Returns:  DataFrame with columns
                osm_id (int), lift_type (str, e.g. "chair_lift", "gondola"), name (str or None),
                coordinates (list of (lat, lon) tuples)
    """
    # TODO [NICO | Task 5] Download all lifts
    # Step 1: Query ways with the key aerialway inside Switzerland, with "out geom;".
    # Step 2: Keep the useful types (chair_lift, gondola, cable_car, drag_lift, t-bar, platter, ...).
    # Hint:   Leave out aerialway=station and aerialway=pylon, they are not lifts.
    # Done when: the table has more than 1000 rows.
    raise NotImplementedError("TODO [NICO | Task 5]: fetch_lifts")


def compute_piste_km(pistes: pd.DataFrame) -> pd.DataFrame:
    """
    Length of each piste in km, calculated from its line geometry.

    Owner:    Nico (Task 5: ski resort information)
    Used by:  scripts/02_build_database.py -> database.save_table(..., "pistes")
    Source:   output of fetch_pistes()
    Returns:  the same DataFrame plus a column length_km (float)
    """
    # TODO [NICO | Task 5] Calculate piste length from geometry
    # Step 1: For each piste, add up the distance between each pair of neighbouring points.
    # Step 2: Use the haversine formula for the distance between two (lat, lon) points.
    #         (The prototype's mock_data.py has a _distance_km function you can learn from.)
    # Step 3: Store the sum in length_km.
    # Hint:   Later, piste km per resort = sum of length_km of all pistes inside the resort area.
    # Done when: a piste with points (46.0, 7.0) and (46.01, 7.0) gets length_km of about 1.11.
    raise NotImplementedError("TODO [NICO | Task 5]: compute_piste_km")
