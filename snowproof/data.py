"""
data.py: everything about getting and storing the data. Download from the APIs, save in SQLite,
clean it, check coverage, link stations to resorts, and create the weekly labels.

Owner:       Nico (Task 3: snow and weather data, Task 4: database and preparation, Task 5: resorts)
             label_good_weeks together with Julian
Depends on:  config.py
Used by:     pipeline.py (steps 1 to 3), model.py, data_access.py (when USE_MOCK_DATA is False)
Flow:        Steps 1 to 3 of 5 (download, database, labels)

Sections in this file (in the order you build them):
  1. MeteoSwiss            measured snow depth = our target
  2. Open-Meteo            historical weather, only for features
  3. OpenStreetMap         resorts, pistes, lifts
  4. SLF                   optional
  5. SQLite database       tables, save, load, cache
  6. Preparation           coverage check, cleaning, station mapping, the 7-day labels

Proposed database tables and columns (use exactly these names, they match all docstrings):

  stations                station_code TEXT PRIMARY KEY, station_name TEXT, lat REAL, lon REAL,
                          altitude_m REAL, canton TEXT, first_year INTEGER, last_year INTEGER
  resorts                 resort_id TEXT PRIMARY KEY, osm_id INTEGER, name TEXT, canton TEXT,
                          lat REAL, lon REAL, base_altitude_m REAL, summit_altitude_m REAL,
                          lifts INTEGER, piste_blue_km REAL, piste_red_km REAL, piste_black_km REAL,
                          total_piste_km REAL, description TEXT
  resort_station_mapping  resort_id TEXT, station_code TEXT (NULL if none), distance_km REAL,
                          altitude_diff_m REAL, is_reliable INTEGER (1 or 0)
  snow_daily              station_code TEXT, date TEXT (YYYY-MM-DD), snow_depth_cm REAL, new_snow_cm REAL,
                          PRIMARY KEY (station_code, date)
  weather_daily           station_code TEXT, date TEXT, temperature_mean_c REAL, snowfall_cm REAL,
                          precipitation_mm REAL, PRIMARY KEY (station_code, date)
  weekly_labels           station_code TEXT, week_start TEXT, season_year INTEGER, calendar_week INTEGER,
                          good_week INTEGER (1, 0 or NULL if unknown)
  pistes                  osm_id INTEGER, resort_id TEXT, difficulty TEXT, length_km REAL
  holiday_periods         canton TEXT, holiday_name TEXT, start_date TEXT, end_date TEXT
  transport_stops         resort_id TEXT, stop_id TEXT, stop_name TEXT, lat REAL, lon REAL, distance_m REAL
  model_runs              run_id TEXT, created_at TEXT, model_name TEXT, round TEXT, train_period TEXT,
                          test_period TEXT, model_accuracy REAL, model_brier REAL,
                          baseline_accuracy REAL, baseline_brier REAL
  weekly_predictions      station_code TEXT, week_start TEXT, calendar_week INTEGER, chance REAL,
                          baseline REAL, PRIMARY KEY (station_code, week_start)

Data sources and attribution: MeteoSwiss Open Data, Open-Meteo (ERA5), © OpenStreetMap contributors.
"""

import sqlite3
from collections.abc import Callable
from datetime import date

import pandas as pd
import requests

from snowproof import config


# ============================================================================
# MeteoSwiss: measured snow depth (our target)
# ============================================================================
# Why MeteoSwiss? This is MEASURED snow depth at real stations, going back decades. A "good week"
# is decided only from this data. Davos has data from 1931 and Weissfluhjoch from 1958, but many
# stations are much shorter.

def list_stations() -> pd.DataFrame:
    """
    List all MeteoSwiss stations that measure snow depth.

    Owner:    Nico (Task 3: snow and weather data collection)
    Used by:  pipeline.py step 1 -> save_table(..., "stations")
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
    Used by:  pipeline.py step 1 -> save_snow_daily()
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


# ============================================================================
# Open-Meteo: historical weather (features only)
# ============================================================================

def fetch_weather(station_code: str, lat: float, lon: float, start: date, end: date) -> pd.DataFrame:
    """
    Download daily historical weather for one location (we use the station's location).

    Owner:    Nico (Task 3: snow and weather data collection)
    Used by:  pipeline.py step 1 -> save_table(..., "weather_daily")
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


# ============================================================================
# OpenStreetMap / Overpass: resorts, pistes, lifts
# ============================================================================
# Why the Swiss instance (config.OVERPASS_URL)? overpass-api.de hung in our tests.
# Cache the results (fetch_with_cache): Overpass is slow and shared by everyone.

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
    Used by:  pipeline.py step 1 -> save_table(..., "resorts")
    Source:   OpenStreetMap via Overpass
    Returns:  DataFrame with columns
                resort_id (str, short and stable, e.g. "davos"), osm_id (int), name (str),
                lat (float), lon (float), canton (str, filled later in pipeline.py step 2)
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
    Used by:  pipeline.py step 1, then compute_piste_km()
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
    # Hint:   This query is big. Run it once and cache it (fetch_with_cache).
    # Done when: the table has thousands of rows and every row has at least 2 coordinates.
    raise NotImplementedError("TODO [NICO | Task 5]: fetch_pistes")


def fetch_lifts() -> pd.DataFrame:
    """
    All ski lifts (aerialways) in Switzerland.

    Owner:    Nico (Task 5: ski resort information)
    Used by:  pipeline.py step 1, then pipeline.py step 2 (count lifts per resort)
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
    Used by:  pipeline.py step 2 -> save_table(..., "pistes")
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


# ============================================================================
# SLF: optional second snow source
# ============================================================================

def fetch_slf_snow_depth(station_code: str, start: date, end: date) -> pd.DataFrame:
    """
    Daily snow depth from one SLF station. OPTIONAL.

    Owner:    Nico (Task 3, optional)
    Used by:  (optional) pipeline.py step 1
    Source:   SLF measurement data (check the SLF data portal for the current download options)
    Returns:  same columns as fetch_snow_depth():
                station_code (str), date (datetime.date), snow_depth_cm (float), new_snow_cm (float)
    """
    # TODO [NICO | Task 3, optional] Second snow source from SLF
    # Step 1: Ask the team first: does the coverage check (check_station_coverage) show
    #         resorts without any good MeteoSwiss station? If not, skip this file.
    # Step 2: Find how SLF offers its station data and the license terms.
    # Step 3: Return exactly the same columns as fetch_snow_depth, so nothing else has to change.
    # Hint:   SLF records usually start in the 1990s, too short for the 1950 to 2025 validation.
    # Done when: the team decided to use it, and the columns match fetch_snow_depth.
    raise NotImplementedError("TODO [NICO | Task 3, optional]: fetch_slf_snow_depth")


# ============================================================================
# SQLite database: tables, save, load, cache
# ============================================================================
# Why SQLite? One file (config.DB_PATH), no server, built into Python, and pandas reads and
# writes it directly. The table plan is at the top of this file.

def get_connection() -> sqlite3.Connection:
    """
    Open a connection to our SQLite file (and create the data folder if needed).

    Owner:    Nico (Task 4: database and data preparation)
    Used by:  every function in this file
    Source:   config.DB_PATH
    Returns:  an open sqlite3.Connection
    """
    # TODO [NICO | Task 4] Open the database connection
    # Step 1: Make sure config.DATA_DIR exists (Path.mkdir with parents=True, exist_ok=True).
    # Step 2: Return sqlite3.connect(config.DB_PATH).
    # Hint:   Close connections when done. "with get_connection() as conn:" commits automatically,
    #         but read the sqlite3 docs: it does NOT close the connection for you.
    # Done when: get_connection() creates data/snowproof.sqlite if it does not exist yet.
    raise NotImplementedError("TODO [NICO | Task 4]: get_connection")


def create_tables() -> None:
    """
    Create all tables listed at the top of this file (only if they do not exist yet).

    Owner:    Nico (Task 4: database and data preparation)
    Used by:  pipeline.py step 2
    Source:   the table list in this file's header
    Returns:  nothing
    """
    # TODO [NICO | Task 4] Write the CREATE TABLE statements
    # Step 1: For each table in the header, write one "CREATE TABLE IF NOT EXISTS ..." statement
    #         with the listed columns and types.
    # Step 2: Run all statements with conn.executescript(...).
    # Hint:   PRIMARY KEY (station_code, date) stops the same day from being saved twice.
    # Hint:   Store dates as TEXT "YYYY-MM-DD". SQLite has no real date type.
    # Done when: after create_tables(), "SELECT name FROM sqlite_master" lists all 11 tables.
    raise NotImplementedError("TODO [NICO | Task 4]: create_tables")


def save_table(df: pd.DataFrame, table_name: str, replace: bool = False) -> None:
    """
    Save a DataFrame into one of our tables.

    Owner:    Nico (Task 4: database and data preparation)
    Used by:  pipeline.py (all steps)
    Source:   any DataFrame whose columns match the table
    Returns:  nothing
    """
    # TODO [NICO | Task 4] Save a DataFrame
    # Step 1: Open a connection with get_connection().
    # Step 2: Use DataFrame.to_sql with if_exists="replace" or "append" depending on `replace`, index=False.
    # Hint:   "replace" deletes the table first, including your PRIMARY KEY definition.
    #         Prefer deleting the rows yourself and then appending.
    # Done when: save_table(df, "stations") followed by load_table("stations") gives the same rows back.
    raise NotImplementedError("TODO [NICO | Task 4]: save_table")


def save_snow_daily(df: pd.DataFrame) -> None:
    """
    Save measured snow depth without creating duplicate days.

    Owner:    Nico (Task 4: database and data preparation)
    Used by:  pipeline.py step 1, pipeline.py step 2
    Source:   output of fetch_snow_depth()
    Returns:  nothing
    """
    # TODO [NICO | Task 4] Save snow data safely
    # Step 1: Turn the date column into "YYYY-MM-DD" text.
    # Step 2: Insert with "INSERT OR REPLACE INTO snow_daily ..." (conn.executemany), so running
    #         the download twice does not create duplicates.
    # Hint:   NaN must be saved as NULL, never as 0 (see the hint in fetch_snow_depth).
    # Done when: saving the same station twice still gives one row per day.
    raise NotImplementedError("TODO [NICO | Task 4]: save_snow_daily")


def load_table(table_name: str, where: str = "", params: tuple = ()) -> pd.DataFrame:
    """
    Load a table (or part of it) into a DataFrame.

    Owner:    Nico (Task 4: database and data preparation)
    Used by:  pipeline.py (all steps), data_access.py
    Source:   our SQLite database
    Returns:  DataFrame with the table's columns (dates as datetime.date where the column is a date)
    """
    # TODO [NICO | Task 4] Load a table
    # Step 1: Build the query: f"SELECT * FROM {table_name}" plus " WHERE " + where if given.
    # Step 2: Run pd.read_sql_query(query, conn, params=params).
    # Step 3: Turn text date columns (date, week_start, start_date, end_date) back into datetime.date.
    # Hint:   Always pass user values through params ("station_code = ?"), never with an f-string.
    #         This protects against SQL injection.
    # Done when: load_table("snow_daily", "station_code = ?", ("DAV",)) returns only Davos rows.
    raise NotImplementedError("TODO [NICO | Task 4]: load_table")


def fetch_with_cache(cache_name: str, fetch_function: Callable, *args) -> pd.DataFrame:
    """
    Download something once, then reuse the saved copy on every later run.

    Owner:    Nico (Task 4: database and data preparation)
    Used by:  pipeline.py step 1 (wrap every big fetch in this)
    Source:   config.RAW_DIR (one file per cache_name)
    Returns:  the DataFrame, either from the cache or freshly downloaded
    """
    # TODO [NICO | Task 4] Cache downloads (tutor feedback: don't download 50+ years on every run)
    # Step 1: Build a file path: config.RAW_DIR / f"{cache_name}.csv" (or .parquet).
    # Step 2: If the file exists, read it and return it.
    # Step 3: Otherwise call fetch_function(*args), save the result to the file, and return it.
    # Hint:   cache_name must be unique, e.g. f"snow_{station_code}_{start.year}_{end.year}".
    # Hint:   Delete the file by hand when you want fresh data.
    # Done when: the second call with the same cache_name returns instantly without internet.
    raise NotImplementedError("TODO [NICO | Task 4]: fetch_with_cache")


# ============================================================================
# Preparation: coverage, cleaning, station mapping, labels
# ============================================================================

def check_station_coverage(snow_daily: pd.DataFrame) -> pd.DataFrame:
    """
    How many winters of snow data does each station have?

    Owner:    Nico (Task 4: database and data preparation)
    Used by:  pipeline.py step 3 (printed for the team), Julian's choice of training years
    Source:   snow_daily table
    Returns:  DataFrame with columns
                station_code (str), first_year (int), last_year (int),
                winters_total (int), winters_complete (int, winters with less than 5% missing days),
                share_missing (float, 0 to 1)
    """
    # TODO [NICO | Task 4] Coverage check (do this FIRST, it decides the training period)
    # Step 1: Keep only the season months (config.SEASON_MONTHS).
    # Step 2: Group by station_code and winter (December counts to the next year's winter).
    # Step 3: Count days and missing days (snow_depth_cm is NaN) per winter.
    # Step 4: Summarise per station: first and last year, number of complete winters.
    # Hint:   Useful pandas: groupby, agg, isna().mean().
    # Hint:   Share the result with Julian: how many stations reach back to the 1950s and 1960s?
    #         If only a few do, WALK_FORWARD_ROUNDS in model.py must change.
    # Done when: the table shows Davos (DAV) starting around 1931 and Weissfluhjoch (WFJ) around 1958.
    raise NotImplementedError("TODO [NICO | Task 4]: check_station_coverage")


def clean_snow_daily(snow_daily: pd.DataFrame) -> pd.DataFrame:
    """
    Remove impossible values and make dates consistent.

    Owner:    Nico (Task 4: database and data preparation)
    Used by:  pipeline.py step 3
    Source:   snow_daily table
    Returns:  same columns as the input: station_code, date, snow_depth_cm, new_snow_cm
    """
    # TODO [NICO | Task 4] Clean the snow data
    # Step 1: Set negative snow depths and absurd values (e.g. above 1000 cm) to NaN.
    # Step 2: Make sure there is exactly one row per station and day (drop duplicates).
    # Step 3: Make sure all dates are Swiss local days. MeteoSwiss and Open-Meteo must use the
    #         same day boundaries (we ask Open-Meteo for timezone="Europe/Zurich").
    # Hint:   Do NOT fill gaps. A gap must stay NaN, so the label can become "unknown".
    # Done when: no negative values remain and the number of NaN days did not shrink.
    raise NotImplementedError("TODO [NICO | Task 4]: clean_snow_daily")


def map_stations_to_resorts(resorts: pd.DataFrame, stations: pd.DataFrame,
                            max_distance_km: float = 15, max_altitude_diff_m: float = 400) -> pd.DataFrame:
    """
    Find the measurement station that speaks for each resort, or none.

    Owner:    Nico (Task 4: database and data preparation)
    Used by:  pipeline.py step 2 -> save_table(..., "resort_station_mapping")
    Source:   resorts and stations tables, plus the coverage check
    Returns:  DataFrame with columns
                resort_id (str), station_code (str or None), distance_km (float or None),
                altitude_diff_m (float or None), is_reliable (bool)
    """
    # TODO [NICO | Task 4] Link stations to resorts
    # Step 1: For each resort, compute the distance to every station (haversine, like compute_piste_km).
    # Step 2: Keep stations within max_distance_km and with a similar altitude
    #         (difference to the resort's base altitude below max_altitude_diff_m).
    # Step 3: Among those, prefer the station with the longest record (from the coverage check).
    # Step 4: If none fits, station_code is None and is_reliable is False.
    #         The app then shows "No reliable measurement station nearby".
    # Hint:   The thresholds are a team decision. Write down why you chose them (for the video).
    # Done when: Davos Klosters is linked to DAV, and some low or remote resorts get no station.
    raise NotImplementedError("TODO [NICO | Task 4]: map_stations_to_resorts")


def label_good_weeks(snow_daily: pd.DataFrame) -> pd.DataFrame:
    """
    The target variable: was a 7-day period a good ski week?

    good_week = 1 if snow_depth_cm >= 50 on ALL 7 days,
                0 if at least one of the 7 days is below 50 cm,
                unknown (NaN) if any day is missing and no day is below 50 cm.

    Owner:    Nico + Julian (Task 4 and Task 6)
    Used by:  pipeline.py step 3 -> save_table(..., "weekly_labels")
    Source:   cleaned snow_daily
    Returns:  DataFrame with columns
                station_code (str), week_start (datetime.date), season_year (int),
                calendar_week (int, ISO week of week_start), good_week (float: 1.0, 0.0 or NaN)
    """
    # TODO [NICO+JULIAN | Task 4] Create the weekly labels (the most important rule of the project)
    # Step 1: Decide as a team which weeks to label: every possible start day (rolling windows),
    #         or fixed weeks (e.g. starting on Saturday, when most holidays start). Write it down.
    # Step 2: Per station, sort by date and look at each window of config.GOOD_WEEK_DAYS days.
    # Step 3: Apply the rule above, using config.GOOD_SNOW_CM. Note the order:
    #         any day below 50 cm -> 0, else any day missing -> unknown, else -> 1.
    # Step 4: Keep only windows inside the season (config.SEASON_MONTHS).
    # Hint:   pandas rolling windows (Series.rolling(7)) can help, but check how they treat NaN.
    # Hint:   A missing day is NOT a bad day. Never fill NaN with 0 here.
    # Hint:   tests/test_labels.py lists the cases this function must pass. Write those tests first.
    # Done when: all cases in tests/test_labels.py pass.
    raise NotImplementedError("TODO [NICO+JULIAN | Task 4]: label_good_weeks")
