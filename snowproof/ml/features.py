"""
features.py: build the model inputs (features). ONLY things known before the holiday starts.

Owner:       Julian (Task 6: model training)
Depends on:  config.py, the weekly_labels, stations and resort tables
Used by:     ml/train.py, ml/evaluate.py, scripts/05_save_predictions.py
Flow:        Step 4 of 5 (train and validate)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! DATA LEAKAGE WARNING                                                                 !!
!! The actual weather or snow of the holiday week must NEVER be an input.               !!
!! When a user asks in October about a week in February, nobody knows that weather yet. !!
!! If you use it, the model looks great in testing and is useless in the app.           !!
!! Rule of thumb: for every feature ask "would I know this on the day the user asks?"   !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

import pandas as pd

# The features the model may use (known in advance). Change this list only together with Jan.
FEATURE_COLUMNS = [
    "altitude_m",             # altitude of the station
    "week_of_season",         # 0 = first week of December, about 21 = end of April
    "region",                 # e.g. canton or a north/south/inner-alpine code (as numbers)
    "year",                   # long-term trend (warming)
    "past_good_week_share",   # share of good weeks for this calendar week in EARLIER years only
]

# Optional, only for predictions made DURING the season (the snow on the day the user asks):
OPTIONAL_IN_SEASON_FEATURES = [
    "current_snow_depth_cm",  # measured on the day of the request, not during the holiday
    "snowfall_last_14_days_cm",
]


def build_features(labels: pd.DataFrame, stations: pd.DataFrame) -> pd.DataFrame:
    """
    One row per labelled week with all FEATURE_COLUMNS plus the target.

    Owner:    Julian (Task 6: model training)
    Used by:  ml/train.py, ml/evaluate.py, scripts/04_train_and_validate.py
    Source:   weekly_labels and stations tables
    Returns:  DataFrame with columns
                station_code (str), week_start (datetime.date), season_year (int),
                all FEATURE_COLUMNS, good_week (float: 1.0 or 0.0; unknown weeks removed)
    """
    # TODO [JULIAN | Task 6] Build the feature table
    # Step 1: Merge labels with stations on station_code to get altitude_m and the region.
    # Step 2: Compute week_of_season from week_start (days since 1 December, divided by 7).
    # Step 3: year = season_year. Turn text columns like region into numbers (pandas get_dummies or a mapping).
    # Step 4: Add past_good_week_share with add_past_good_week_share() below.
    # Step 5: Drop rows where good_week is unknown (NaN). The model can only learn from known weeks.
    # Hint:   Re-read the leakage warning at the top before adding ANY new column.
    # Done when: the table has no NaN in FEATURE_COLUMNS or good_week, and one row per labelled week.
    raise NotImplementedError("TODO [JULIAN | Task 6]: build_features")


def add_past_good_week_share(features: pd.DataFrame) -> pd.DataFrame:
    """
    For each row: the share of good weeks at this station and calendar week in EARLIER years only.

    Owner:    Julian (Task 6: model training)
    Used by:  build_features()
    Source:   the feature table itself (good_week of previous years)
    Returns:  the same DataFrame plus a column past_good_week_share (float, 0 to 1, NaN if no earlier years)
    """
    # TODO [JULIAN | Task 6] Past share of good weeks (without looking into the future)
    # Step 1: Sort by station_code, calendar_week and season_year.
    # Step 2: For each row, average good_week over the SAME station and calendar week in EARLIER years.
    # Step 3: Decide what to do with the first years (no history yet): drop them or use a default.
    # Hint:   groupby(...).transform with expanding().mean() and shift(1) does "earlier years only".
    #         Without shift(1) the current year leaks into its own feature.
    # Done when: for the first year of a station the value is NaN, and it never uses the same or later years.
    raise NotImplementedError("TODO [JULIAN | Task 6]: add_past_good_week_share")
