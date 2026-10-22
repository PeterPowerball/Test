"""
evaluate.py: walk-forward validation. Train on the past, test on the next decade, repeat.

Owner:       Julian (Task 7: model evaluation and prediction function)
Depends on:  ml/features.py, ml/baseline.py, ml/train.py
Used by:     scripts/04_train_and_validate.py
Flow:        Step 4 of 5 (train and validate)

Why walk-forward? A random train/test split would let the model learn from 2010 and be
tested on 1990, which is like knowing the future. Walk-forward always tests on LATER years.
"""

import pandas as pd

# (name, (train_from, train_to), (test_from, test_to)). All years inclusive.
# Hint: these years may need to change after Nico's coverage check
#       (preparation.check_station_coverage). If few stations reach back to 1950, start later.
WALK_FORWARD_ROUNDS = [
    ("Round 1", (1950, 1969), (1970, 1979)),
    ("Round 2", (1950, 1979), (1980, 1989)),
    ("Round 3", (1950, 1989), (1990, 1999)),
    ("Round 4", (1950, 1999), (2000, 2009)),
]
# The final check is used ONLY ONCE, at the very end, and NEVER for tuning (choosing models or settings).
FINAL_CHECK = ("Final check", (1950, 2014), (2015, 2025))


def split_by_years(features: pd.DataFrame, train_years: tuple[int, int],
                   test_years: tuple[int, int]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split the feature table into a training part and a test part by season_year.

    Owner:    Julian (Task 7: model evaluation and prediction function)
    Used by:  run_walk_forward()
    Source:   output of features.build_features()
    Returns:  (train_df, test_df), both with the same columns as the input
    """
    # TODO [JULIAN | Task 7] Split by years
    # Step 1: train_df = rows with season_year between train_years[0] and train_years[1].
    # Step 2: test_df = rows with season_year between test_years[0] and test_years[1].
    # Hint:   Series.between(a, b) includes both ends.
    # Done when: no season_year appears in both parts.
    raise NotImplementedError("TODO [JULIAN | Task 7]: split_by_years")


def compute_metrics(y_true: pd.Series, y_prob: pd.Series) -> dict:
    """
    Accuracy and Brier score for predicted probabilities.

    Owner:    Julian (Task 7: model evaluation and prediction function)
    Used by:  run_walk_forward()
    Source:   true labels (0 or 1) and predicted chances (0 to 1)
    Returns:  dict with keys accuracy (float, higher is better), brier (float, lower is better)
    """
    # TODO [JULIAN | Task 7] Metrics
    # Step 1: Accuracy: turn probabilities into yes/no with a 0.5 cut-off, then compare with y_true.
    # Step 2: Brier score: mean of (probability minus true label) squared.
    # Hint:   scikit-learn has sklearn.metrics.accuracy_score and sklearn.metrics.brier_score_loss.
    # Done when: perfect predictions give accuracy 1.0 and brier 0.0.
    raise NotImplementedError("TODO [JULIAN | Task 7]: compute_metrics")


def run_walk_forward(features: pd.DataFrame, labels: pd.DataFrame, model_name: str,
                     include_final_check: bool = False) -> pd.DataFrame:
    """
    Run all walk-forward rounds for one model and compare it with the baseline.

    Owner:    Julian (Task 7: model evaluation and prediction function)
    Used by:  scripts/04_train_and_validate.py -> database.save_table(..., "model_runs")
    Source:   features (ml/features.py), labels (for the baseline)
    Returns:  DataFrame with one row per round and columns
                round, train_period ("1950-1969"), test_period, model_accuracy, baseline_accuracy,
                model_brier, baseline_brier
              (the same columns as data_access.get_validation_results(), so the app can show it)
    """
    # TODO [JULIAN | Task 7] Walk-forward validation
    # Step 1: Loop over WALK_FORWARD_ROUNDS (and FINAL_CHECK only if include_final_check is True).
    # Step 2: In each round: split_by_years, train with train.train_model on the train part only.
    # Step 3: Predict chances for the test part, compute_metrics for the model.
    # Step 4: compute the baseline (baseline.compute_baseline) on the TRAIN years, use it as the
    #         prediction for the test weeks, and compute_metrics for the baseline too.
    # Step 5: Collect one row per round in a list of dicts, return pd.DataFrame(rows).
    # Hint:   Never let the test years touch training, the baseline or past_good_week_share.
    # Done when: you get 4 rows (5 with the final check), and the model's Brier is lower than the baseline's.
    raise NotImplementedError("TODO [JULIAN | Task 7]: run_walk_forward")
