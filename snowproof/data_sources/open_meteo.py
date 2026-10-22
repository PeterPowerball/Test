"""
open_meteo.py: download historical weather (ERA5) from Open-Meteo, used as model FEATURES.

Owner:       Nico (Task 3: snow and weather data collection)
Depends on:  config.py
Used by:     scripts/01_download_data.py
Flow:        Step 1 of 5 (download data)

Why Open-Meteo? It gives daily temperature and snowfall for any point since 1950,
also where there is no station. We use it only for features, never as the target.
"""

from datetime import date

import pandas as pd
import requests

from snowproof import config


def fetch_weather(station_code: str, lat: float, lon: float, start: date, end: date) -> pd.DataFrame:
    """
    Download daily historical weather for one location (we use the station's location).

    Owner:    Nico (Task 3: snow and weather data collection)
    Used by:  scripts/01_download_data.py -> database.save_table(..., "weather_daily")
    Source:   Open-Meteo Historical Weather API (ERA5), config.OPEN_METEO_ARCHIVE_URL
    Returns:  DataFrame with columns
                station_code (str), date (datetime.date),
                temperature_mean_c (float), snowfall_cm (float), precipitation_mm (float)
    """
    # TODO [NICO | Task 3] Download historical weather from Open-Meteo
    # Step 1: Build the request parameters: latitude, longitude, start_date, end_date
    #         (format "YYYY-MM-DD"), daily=",".join(config.OPEN_METEO_DAILY_VARIABLES),
    #         timezone="Europe/Zurich".
    #         Example URL: .../v1/archive?latitude=46.8&longitude=9.83&start_date=2020-01-01&end_date=2020-01-31&daily=snowfall_sum
    # Step 2: Call requests.get(config.OPEN_METEO_ARCHIVE_URL, params=..., timeout=...).
    # Step 3: The answer is JSON. The values are in response.json()["daily"]. Turn it into a DataFrame.
    # Step 4: Rename the columns to the names above and add the station_code column.
    # Hint:   Ask for long periods in chunks (e.g. 10 years per call). The API limits big requests.
    # Hint:   NEVER use Open-Meteo's modelled "snow_depth" as the target. It was about 42 cm off
    #         at Davos in January 2025. Our target always comes from MeteoSwiss measurements.
    # Hint:   Always pass timezone="Europe/Zurich", so the days match the MeteoSwiss days.
    # Done when: fetch_weather("DAV", 46.81, 9.84, date(2020,1,1), date(2020,1,31)) returns 31 rows.
    raise NotImplementedError("TODO [NICO | Task 3]: fetch_weather")
