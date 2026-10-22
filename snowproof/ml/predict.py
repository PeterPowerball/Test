"""
predict.py: the prediction function the app uses.

Owner:       Julian (Task 7: model evaluation and prediction function)
Depends on:  ml/features.py, ml/train.py, database.py (weekly_predictions, resort_station_mapping)
Used by:     scripts/05_save_predictions.py, data_access.predict_good_week()
Flow:        Step 5 of 5 (precompute predictions), then live in the app

How it works: script 05 computes the chance for every station and every possible week start
of the coming season ONCE and stores it in the weekly_predictions table. The app then only
looks up numbers, which is fast and never trains anything.
"""

from datetime import date

import pandas as pd


def predict_chance(model, station: dict, week_start: date, past_good_week_share: float) -> float:
    """
    Chance of a good week for one station and one week start (used by script 05).

    Owner:    Julian (Task 7: model evaluation and prediction function)
    Used by:  scripts/05_save_predictions.py
    Source:   the trained model, station facts (altitude_m, region), past share from weekly_labels
    Returns:  chance between 0 and 1 (float)
    """
    # TODO [JULIAN | Task 7] One prediction
    # Step 1: Build ONE row with exactly the features.FEATURE_COLUMNS, in the same way as build_features
    #         (week_of_season from week_start, year = the coming season, altitude, region, past share).
    # Step 2: Return model.predict_proba(row)[0, 1].
    # Hint:   Reuse the helper logic from features.py, so training and prediction build features the same way.
    # Done when: a high station in mid-February gets a higher chance than a low station in December.
    raise NotImplementedError("TODO [JULIAN | Task 7]: predict_chance")


def predict_good_week(resort_id: str, start_date: date, end_date: date) -> dict:
    """
    Chance of a good ski week for a stay at one resort (used by the app).

    Owner:    Julian (Task 7: model evaluation and prediction function)
    Used by:  data_access.predict_good_week()
    Source:   weekly_predictions and resort_station_mapping tables (filled by script 05)
    Returns:  dict with the SAME keys as the prototype (see mock_access.predict_good_week):
                available (bool), reason (str, only if not available),
                chance (float 0 to 1, mean over the weeks of the stay),
                baseline (float 0 to 1, historical average for the same weeks),
                weekly (DataFrame: label, week_start, week_end, chance, baseline),
                daily (DataFrame: date, expected_cm, low_cm, high_cm), station_code (str)
    """
    # TODO [JULIAN | Task 7] Prediction for a stay
    # Step 1: Look up the resort's station in resort_station_mapping. No reliable station ->
    #         return {"available": False, "reason": "No reliable measurement station nearby."}.
    # Step 2: Cut the stay into blocks of config.GOOD_WEEK_DAYS days (the prototype's
    #         mock_data.split_into_weeks shows the idea).
    # Step 3: For each block, read chance and baseline from weekly_predictions (station_code, week_start).
    # Step 4: Return the dict above. chance and baseline are the means over the blocks.
    # Hint:   "daily" (expected snow depth per day for the chart) needs its own idea: e.g. the median
    #         measured depth per calendar day in recent years, with the 10% and 90% values as the band.
    #         Agree on this with Noah, who draws the chart.
    # Done when: the snow check page shows the same layout as with mock data, but real numbers.
    raise NotImplementedError("TODO [JULIAN | Task 7]: predict_good_week")
