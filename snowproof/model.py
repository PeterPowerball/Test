"""
model.py: our own machine learning model. Features, baseline, training, walk-forward evaluation, prediction.

Owner:       Julian (Task 6: model training, Task 7: evaluation and prediction function)
             Jan supports training and the model comparison
Depends on:  config.py, data.py (weekly_labels, stations, weekly_predictions tables)
Used by:     pipeline.py (steps 4 and 5), data_access.py
Flow:        Steps 4 and 5 of 5 (train and validate, save predictions)

Sections in this file (in the order you build them):
  1. Features     what the model gets as input (read the leakage warning!)
  2. Baseline     the historical average the model must beat
  3. Training     candidate models, choose the best, save and load
  4. Evaluation   walk-forward validation
  5. Prediction   chances for the app

Training happens ONLY in pipeline.py, never inside the Streamlit app (it would be far too slow).

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! DATA LEAKAGE WARNING                                                                 !!
!! The actual weather or snow of the holiday week must NEVER be an input.               !!
!! When a user asks in October about a week in February, nobody knows that weather yet. !!
!! If you use it, the model looks great in testing and is useless in the app.           !!
!! Rule of thumb: for every feature ask "would I know this on the day the user asks?"   !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

from datetime import date

import joblib
import pandas as pd

from snowproof import config


# ============================================================================
# Features: model inputs known in advance
# ============================================================================

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
    Used by:  run_walk_forward(), pipeline.py step 4
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


# ============================================================================
# Baseline: the historical average to beat
# ============================================================================
# Why? "In the past, 61% of these weeks were good" is the obvious guess anyone can make.
# If our model is not better than that, it adds nothing. Graders will ask about this.

def compute_baseline(labels: pd.DataFrame, train_years: tuple[int, int]) -> pd.DataFrame:
    """
    Historical share of good weeks per station and calendar week, using only the training years.

    Owner:    Julian (Task 6: model training)
    Used by:  run_walk_forward(), pipeline.py step 5
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


# ============================================================================
# Training: candidate models, choose the best, save
# ============================================================================

# Models to compare (names only, you create them in make_model). Add more if you like.
CANDIDATE_MODELS = ["logistic_regression", "random_forest"]


def make_model(model_name: str):
    """
    Create an untrained scikit-learn model by name.

    Owner:    Julian (Task 6: model training)
    Used by:  train_model()
    Source:   scikit-learn
    Returns:  an unfitted scikit-learn classifier
    """
    # TODO [JULIAN | Task 6] Create the candidate models
    # Step 1: "logistic_regression" -> sklearn.linear_model.LogisticRegression (raise max_iter).
    # Step 2: "random_forest" -> sklearn.ensemble.RandomForestClassifier (set random_state=config.RANDOM_SEED).
    # Step 3: Raise a ValueError for unknown names.
    # Hint:   Logistic regression works better with scaled inputs: look at sklearn.pipeline.make_pipeline
    #         together with sklearn.preprocessing.StandardScaler.
    # Done when: make_model("random_forest") returns a model with a fit and a predict_proba method.
    raise NotImplementedError("TODO [JULIAN | Task 6]: make_model")


def train_model(train_df: pd.DataFrame, model_name: str):
    """
    Fit one model on the training rows.

    Owner:    Julian + Jan (Task 6: model training)
    Used by:  run_walk_forward(), pipeline.py step 4
    Source:   feature table (FEATURE_COLUMNS and good_week)
    Returns:  the fitted model
    """
    # TODO [JULIAN+JAN | Task 6] Train a model
    # Step 1: X = train_df[FEATURE_COLUMNS], y = train_df["good_week"].astype(int).
    # Step 2: model = make_model(model_name), then model.fit(X, y).
    # Hint:   Good weeks may be rare at low stations. Check the class balance with y.mean().
    # Done when: model.predict_proba(X)[:, 1] returns one chance between 0 and 1 per row.
    raise NotImplementedError("TODO [JULIAN+JAN | Task 6]: train_model")


def choose_best_model(validation_results: dict[str, pd.DataFrame]) -> str:
    """
    Pick the model with the best average Brier score over the walk-forward rounds.

    Owner:    Julian + Jan (Task 6: model training)
    Used by:  pipeline.py step 4
    Source:   {model_name: output of run_walk_forward()} (WITHOUT the final check)
    Returns:  the name of the best model (str)
    """
    # TODO [JULIAN+JAN | Task 6] Choose the best model
    # Step 1: For each model, average model_brier over the rounds.
    # Step 2: Return the name with the lowest average (lower Brier is better).
    # Hint:   Decide only on the walk-forward rounds. The final check must not influence this choice.
    # Done when: the function returns one of CANDIDATE_MODELS, and you can explain why in the video.
    raise NotImplementedError("TODO [JULIAN+JAN | Task 6]: choose_best_model")


def save_model(model, path=config.MODEL_PATH) -> None:
    """
    Save the trained model to the models/ folder.

    Owner:    Julian (Task 6: model training)
    Used by:  pipeline.py step 4
    Source:   a fitted model
    Returns:  nothing
    """
    # TODO [JULIAN | Task 6] Save the model
    # Step 1: Create config.MODELS_DIR if needed.
    # Step 2: joblib.dump(model, path).
    # Hint:   The .joblib file is gitignored. Precomputed predictions (step 5) are what the app needs.
    # Done when: models/good_week_model.joblib exists after running pipeline.py step 4.
    raise NotImplementedError("TODO [JULIAN | Task 6]: save_model")


def load_model(path=config.MODEL_PATH):
    """
    Load the saved model.

    Owner:    Julian (Task 6: model training)
    Used by:  pipeline.py step 5
    Source:   models/good_week_model.joblib
    Returns:  the fitted model
    """
    # TODO [JULIAN | Task 6] Load the model
    # Step 1: return joblib.load(path).
    # Hint:   Give a clear error message if the file does not exist yet ("run pipeline.py step 4 first").
    # Done when: load_model() returns the same model you saved.
    raise NotImplementedError("TODO [JULIAN | Task 6]: load_model")


# ============================================================================
# Evaluation: walk-forward validation
# ============================================================================
# Why walk-forward? A random train/test split would let the model learn from 2010 and be tested
# on 1990, which is like knowing the future. Walk-forward always tests on LATER years.

# (name, (train_from, train_to), (test_from, test_to)). All years inclusive.
# Hint: these years may need to change after Nico's coverage check
#       (data.check_station_coverage). If few stations reach back to 1950, start later.
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
    Source:   output of build_features()
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
    Used by:  pipeline.py step 4 -> data.save_table(..., "model_runs")
    Source:   features (build_features()), labels (for the baseline)
    Returns:  DataFrame with one row per round and columns
                round, train_period ("1950-1969"), test_period, model_accuracy, baseline_accuracy,
                model_brier, baseline_brier
              (the same columns as data_access.get_validation_results(), so the app can show it)
    """
    # TODO [JULIAN | Task 7] Walk-forward validation
    # Step 1: Loop over WALK_FORWARD_ROUNDS (and FINAL_CHECK only if include_final_check is True).
    # Step 2: In each round: split_by_years, train with train_model on the train part only.
    # Step 3: Predict chances for the test part, compute_metrics for the model.
    # Step 4: compute the baseline (compute_baseline) on the TRAIN years, use it as the
    #         prediction for the test weeks, and compute_metrics for the baseline too.
    # Step 5: Collect one row per round in a list of dicts, return pd.DataFrame(rows).
    # Hint:   Never let the test years touch training, the baseline or past_good_week_share.
    # Done when: you get 4 rows (5 with the final check), and the model's Brier is lower than the baseline's.
    raise NotImplementedError("TODO [JULIAN | Task 7]: run_walk_forward")


# ============================================================================
# Prediction: chances for the app
# ============================================================================
# pipeline.py step 5 computes the chance for every station and every possible week start of the
# coming season ONCE and stores it in weekly_predictions. The app then only looks up numbers.

def predict_chance(model, station: dict, week_start: date, past_good_week_share: float) -> float:
    """
    Chance of a good week for one station and one week start (used by pipeline.py step 5).

    Owner:    Julian (Task 7: model evaluation and prediction function)
    Used by:  pipeline.py step 5
    Source:   the trained model, station facts (altitude_m, region), past share from weekly_labels
    Returns:  chance between 0 and 1 (float)
    """
    # TODO [JULIAN | Task 7] One prediction
    # Step 1: Build ONE row with exactly the FEATURE_COLUMNS, in the same way as build_features
    #         (week_of_season from week_start, year = the coming season, altitude, region, past share).
    # Step 2: Return model.predict_proba(row)[0, 1].
    # Hint:   Reuse the feature helpers from section 1, so training and prediction build features the same way.
    # Done when: a high station in mid-February gets a higher chance than a low station in December.
    raise NotImplementedError("TODO [JULIAN | Task 7]: predict_chance")


def predict_good_week(resort_id: str, start_date: date, end_date: date) -> dict:
    """
    Chance of a good ski week for a stay at one resort (used by the app).

    Owner:    Julian (Task 7: model evaluation and prediction function)
    Used by:  data_access.predict_good_week()
    Source:   weekly_predictions and resort_station_mapping tables (filled by pipeline.py step 5)
    Returns:  dict with the SAME keys as the prototype (see mock_data.predict_good_week):
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
