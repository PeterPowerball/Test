"""
baseline.py: the simple historical baseline our model must beat.

Owner:       Julian (Task 6: model training)
Depends on:  the weekly_labels table
Used by:     ml/evaluate.py (comparison), scripts/05_save_predictions.py, the app ("historical average")
Flow:        Step 4 of 5 (train and validate)

Why a baseline? "In the past, 61% of these weeks were good" is the obvious guess anyone can make.
If our model is not better than that, the model adds nothing. Graders will ask about this.
"""

import pandas as pd


def compute_baseline(labels: pd.DataFrame, train_years: tuple[int, int]) -> pd.DataFrame:
    """
    Historical share of good weeks per station and calendar week, using only the training years.

    Owner:    Julian (Task 6: model training)
    Used by:  ml/evaluate.py, scripts/05_save_predictions.py
    Source:   weekly_labels (good_week 1 or 0; unknown weeks ignored)
    Returns:  DataFrame with columns
                station_code (str), calendar_week (int), baseline_share (float, 0 to 1), n_years (int)
    """
    # TODO [JULIAN | Task 6] Historical baseline
    # Step 1: Keep only rows with season_year between train_years[0] and train_years[1] (both included).
    # Step 2: Drop unknown weeks (good_week is NaN).
    # Step 3: Group by station_code and calendar_week, take the mean of good_week and count the years.
    # Hint:   Only use the training years, otherwise the baseline "knows" the test period.
    # Done when: compute_baseline(labels, (1950, 1969)) gives values between 0 and 1 for every week.
    raise NotImplementedError("TODO [JULIAN | Task 6]: compute_baseline")


def share_per_decade(labels: pd.DataFrame, station_code: str, calendar_week: int) -> pd.DataFrame:
    """
    OPTIONAL (decade chart): share of good weeks per decade for one station and calendar week.

    Owner:    Julian (Task 6, optional)
    Used by:  data_access.get_historical_good_week_share() (optional decade trend chart)
    Source:   weekly_labels
    Returns:  DataFrame with columns decade (str, e.g. "1950s"), share (float, 0 to 1)
    """
    # TODO [JULIAN | Task 6, optional] Share of good weeks per decade
    # Step 1: Filter to one station and calendar week, drop unknown weeks.
    # Step 2: Make a decade column (season_year // 10 * 10) and average good_week per decade.
    # Hint:   The decade chart was removed from the prototype after feedback. Only do this if the team wants it back.
    # Done when: the result has one row per decade with data.
    raise NotImplementedError("TODO [JULIAN | Task 6, optional]: share_per_decade")
