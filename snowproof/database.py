"""
database.py: our SQLite database. Create the tables, save data, load data, cache downloads.

Owner:       Nico (Task 4: database and data preparation)
Depends on:  config.py (DB_PATH, RAW_DIR)
Used by:     all scripts (steps 1 to 5), data_access.py (when USE_MOCK_DATA is False)
Flow:        Step 2 of 5 (build database), then read by every later step and the app

Why SQLite? It is one file (config.DB_PATH), needs no server, is built into Python (sqlite3),
and pandas can read and write it directly. It also lets us show "data via database" for grading.

Proposed tables and columns (use exactly these names, they match all docstrings):

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
"""

import sqlite3
from collections.abc import Callable

import pandas as pd

from snowproof import config


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
    Used by:  scripts/02_build_database.py
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
    Used by:  all scripts
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
    Used by:  scripts/01_download_data.py, scripts/02_build_database.py
    Source:   output of meteoswiss.fetch_snow_depth()
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
    Used by:  all scripts, data_access.py
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
    Used by:  scripts/01_download_data.py (wrap every big fetch in this)
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
