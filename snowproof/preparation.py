"""
preparation.py: clean the raw data, check coverage, link stations to resorts, create the weekly labels.

Owner:       Nico (Task 4: database and data preparation), labels together with Julian
Depends on:  config.py, database.py
Used by:     scripts/02_build_database.py, scripts/03_prepare_labels.py
Flow:        Steps 2 and 3 of 5

Order matters. Do it like this:
  1. check_station_coverage()   decides the training period (how far back do we have data?)
  2. clean_snow_daily()         removes impossible values, keeps gaps as NaN
  3. map_stations_to_resorts()  which station speaks for which resort
  4. label_good_weeks()         the target variable: 1, 0 or unknown
"""

import pandas as pd

from snowproof import config


def check_station_coverage(snow_daily: pd.DataFrame) -> pd.DataFrame:
    """
    How many winters of snow data does each station have?

    Owner:    Nico (Task 4: database and data preparation)
    Used by:  scripts/03_prepare_labels.py (printed for the team), Julian's choice of training years
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
    #         If only a few do, the walk-forward years in ml/evaluate.py must change.
    # Done when: the table shows Davos (DAV) starting around 1931 and Weissfluhjoch (WFJ) around 1958.
    raise NotImplementedError("TODO [NICO | Task 4]: check_station_coverage")


def clean_snow_daily(snow_daily: pd.DataFrame) -> pd.DataFrame:
    """
    Remove impossible values and make dates consistent.

    Owner:    Nico (Task 4: database and data preparation)
    Used by:  scripts/03_prepare_labels.py
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
    Used by:  scripts/02_build_database.py -> database.save_table(..., "resort_station_mapping")
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
    Used by:  scripts/03_prepare_labels.py -> database.save_table(..., "weekly_labels")
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
