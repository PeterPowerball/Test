"""
05_save_predictions.py: precompute the chances for the coming season, for the app. STEP 5 OF 5.

Owner:       Julian + Jan (Task 7 and Task 9)
Depends on:  snowproof/ml/predict.py, snowproof/ml/baseline.py, snowproof/ml/train.py, database.py
Used by:     run by hand: python scripts/05_save_predictions.py
Flow:        Step 5 of 5. Before: 04_train_and_validate.py. After this, Fabio can set USE_MOCK_DATA = False.

Why precompute? The app should only look up numbers. Loading a model and building features
on every click would be slow, and the model must never be trained inside the app.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from snowproof import database  # noqa: E402
from snowproof.ml import baseline, predict, train  # noqa: E402


def main() -> None:
    """
    For every station and every possible week start of the coming season: chance and baseline.

    Owner:    Julian + Jan (Task 7 and Task 9)
    Used by:  run by hand
    Returns:  nothing (fills the weekly_predictions table)
    """
    # TODO [JULIAN+JAN | Task 7] Precompute predictions
    # Step 1: model = train.load_model(). Load stations that have a reliable resort mapping.
    # Step 2: For each station and each day from 1 December to 24 April of the coming season
    #         (each day is a possible week start): chance = predict.predict_chance(...).
    # Step 3: baseline: baseline.compute_baseline(labels, (first year, last year)) for the same calendar week.
    # Step 4: Save everything to weekly_predictions (station_code, week_start, calendar_week, chance, baseline).
    # Done when: weekly_predictions has about 145 rows per station, and the app shows them
    #            after setting config.USE_MOCK_DATA = False.
    raise NotImplementedError("TODO [JULIAN+JAN | Task 7]: 05_save_predictions.main")


if __name__ == "__main__":
    main()
