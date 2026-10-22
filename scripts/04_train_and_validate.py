"""
04_train_and_validate.py: walk-forward validation, choose the best model, final check, save. STEP 4 OF 5.

Owner:       Julian (Task 6 and 7), Jan supports (model comparison)
Depends on:  snowproof/ml/*.py, snowproof/database.py
Used by:     run by hand: python scripts/04_train_and_validate.py
Flow:        Step 4 of 5. Before: 03_prepare_labels.py. Next: 05_save_predictions.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from snowproof import database  # noqa: E402
from snowproof.ml import evaluate, features, train  # noqa: E402


def main() -> None:
    """
    Compare the candidate models with walk-forward validation, run the final check once, save the model.

    Owner:    Julian (Task 6 and 7), Jan (support)
    Used by:  run by hand
    Returns:  nothing
    """
    # TODO [JULIAN | Task 7] Train and validate
    # Step 1: Load weekly_labels and stations, build the feature table (features.build_features).
    # Step 2: For each name in train.CANDIDATE_MODELS: evaluate.run_walk_forward(...) WITHOUT the final check.
    # Step 3: best = train.choose_best_model(results). Print all results so you can compare.
    # Step 4: Only now, ONCE: run the final check for the best model (include_final_check=True).
    # Step 5: Save the rounds to the model_runs table (database.save_table) for the "About our model" page.
    # Step 6: Train the best model on ALL years and save it (train.save_model).
    # Hint:   If you go back and change the model after seeing the final check, the final check
    #         is no longer honest. Write down in GENAI_LOG.md / the video what you did.
    # Done when: models/good_week_model.joblib exists and model_runs has 5 rows for the final model.
    raise NotImplementedError("TODO [JULIAN | Task 7]: 04_train_and_validate.main")


if __name__ == "__main__":
    main()
