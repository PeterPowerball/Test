"""
meteoswiss.py: download measured snow depth from MeteoSwiss Open Data.

Owner:       Nico (Task 3: snow and weather data collection)
Depends on:  config.py (URLs and column names)
Used by:     scripts/01_download_data.py
Flow:        Step 1 of 5 (download data)

Why MeteoSwiss? This is MEASURED snow depth at real stations, going back decades.
It is our training target: a "good week" is decided only from this data.
Davos has data from 1931 and Weissfluhjoch from 1958, but many stations are much shorter.
"""

from datetime import date

import pandas as pd
import requests

from snowproof import config


def list_stations() -> pd.DataFrame:
    """
    List all MeteoSwiss stations that measure snow depth.

    Owner:    Nico (Task 3: snow and weather data collection)
    Used by:  scripts/01_download_data.py -> database.save_table(..., "stations")
    Source:   MeteoSwiss Open Data, STAC collection ch.meteoschweiz.ogd-nime (station metadata CSV)
    Returns:  DataFrame with columns
                station_code (str, e.g. "DAV"), station_name (str),
                lat (float, degrees), lon (float, degrees), altitude_m (float), canton (str)
    """
    # TODO [NICO | Task 3] List all snow measuring stations
    # Step 1: Open the collection in your browser first to understand it:
    #         f"{config.METEOSWISS_STAC_URL}/collections/{config.METEOSWISS_COLLECTION}"
    #         Look at "assets": one of them is the station metadata CSV.
    # Step 2: Download that CSV with requests.get(..., timeout=config.REQUEST_TIMEOUT_SECONDS)
    #         and read it with pandas (pd.read_csv on io.StringIO(response.text)).
    # Step 3: Rename the columns to the names in the docstring above.
    # Step 4: Keep only stations that actually measure snow depth.
    # Hint:   The CSV files use ";" as separator and may use latin-1 encoding.
    # Hint:   Coordinates may come in LV95 (big numbers like 2'600'000). We need lat/lon degrees.
    # Done when: list_stations() returns a table that contains "DAV" (Davos) with altitude about 1594 m.
    raise NotImplementedError("TODO [NICO | Task 3]: list_stations")


def fetch_snow_depth(station_code: str, start: date, end: date) -> pd.DataFrame:
    """
    Download daily measured snow depth for one MeteoSwiss station.

    Owner:    Nico (Task 3: snow and weather data collection)
    Used by:  scripts/01_download_data.py -> database.save_snow_daily()
    Source:   MeteoSwiss Open Data, STAC collection ch.meteoschweiz.ogd-nime
    Returns:  DataFrame with columns
                station_code (str), date (datetime.date),
                snow_depth_cm (float, NaN if missing), new_snow_cm (float, NaN if missing)
    """
    # TODO [NICO | Task 3] Download measured snow depth from MeteoSwiss
    # Step 1: Find the station's historical daily CSV in the STAC collection
    #         (base URL in config.METEOSWISS_STAC_URL). Item URL idea:
    #         f"{config.METEOSWISS_STAC_URL}/collections/{config.METEOSWISS_COLLECTION}/items/{station_code.lower()}"
    # Step 2: Download it with requests and read it with pandas.
    # Step 3: Keep only the snow depth (hto000d0) and new snow (hns000d0) columns,
    #         and rename them to the column names above.
    # Step 4: Turn the date column into datetime.date and filter to the dates between start and end.
    # Hint:   A missing day must stay NaN. Never fill it with 0, because 0 cm
    #         would wrongly turn the week into a "bad week".
    # Hint:   There are separate files for "historical" and "recent" data. You may need both.
    # Done when: fetch_snow_depth("DAV", date(2020,1,1), date(2020,12,31))
    #            returns 366 rows with the columns above.
    raise NotImplementedError("TODO [NICO | Task 3]: fetch_snow_depth")
