"""
train.py: train several scikit-learn models, pick the best one, save it.

Owner:       Julian + Jan (Task 6: model training; Jan supports)
Depends on:  ml/features.py (FEATURE_COLUMNS), config.py (MODEL_PATH, RANDOM_SEED)
Used by:     ml/evaluate.py, scripts/04_train_and_validate.py, scripts/05_save_predictions.py
Flow:        Step 4 of 5 (train and validate)

Training happens ONLY in the scripts, never inside the Streamlit app (it would be far too slow).
Our tutor suggested trying several models and comparing them. That comparison is part of our grade.
"""

import joblib
import pandas as pd

from snowproof import config

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
    Used by:  ml/evaluate.py, scripts/04_train_and_validate.py
    Source:   feature table (features.FEATURE_COLUMNS and good_week)
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
    Used by:  scripts/04_train_and_validate.py
    Source:   {model_name: output of evaluate.run_walk_forward()} (WITHOUT the final check)
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
    Used by:  scripts/04_train_and_validate.py
    Source:   a fitted model
    Returns:  nothing
    """
    # TODO [JULIAN | Task 6] Save the model
    # Step 1: Create config.MODELS_DIR if needed.
    # Step 2: joblib.dump(model, path).
    # Hint:   The .joblib file is gitignored. Precomputed predictions (step 5) are what the app needs.
    # Done when: models/good_week_model.joblib exists after running script 04.
    raise NotImplementedError("TODO [JULIAN | Task 6]: save_model")


def load_model(path=config.MODEL_PATH):
    """
    Load the saved model.

    Owner:    Julian (Task 6: model training)
    Used by:  scripts/05_save_predictions.py
    Source:   models/good_week_model.joblib
    Returns:  the fitted model
    """
    # TODO [JULIAN | Task 6] Load the model
    # Step 1: return joblib.load(path).
    # Hint:   Give a clear error message if the file does not exist yet ("run script 04 first").
    # Done when: load_model() returns the same model you saved.
    raise NotImplementedError("TODO [JULIAN | Task 6]: load_model")
