"""
swisstopo.py: find a place (city or village) and look up altitudes with the geo.admin.ch API.

Owner:       Jan (Task 8: location, travel and holiday filters)
Depends on:  config.py
Used by:     data_access.get_travel_time_minutes(), preparation (resort altitudes)
Flow:        Step 1 of 5 (download data), and live in the app for the user's city / village

The app only asks for a city or village (no street address), to protect the user's privacy.
"""

import requests

from snowproof import config


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
    Used by:  preparation (base and summit altitude of resorts), station checks
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
