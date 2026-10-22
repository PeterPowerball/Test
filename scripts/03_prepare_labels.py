"""
03_prepare_labels.py: check coverage, clean the snow data, create the weekly labels. STEP 3 OF 5.

Owner:       Nico + Julian (Task 4 and Task 6)
Depends on:  snowproof/preparation.py, snowproof/database.py
Used by:     run by hand: python scripts/03_prepare_labels.py
Flow:        Step 3 of 5. Before: 02_build_database.py. Next: 04_train_and_validate.py

The labels are the hand-over point from data (Nico) to model (Julian). Do this together.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from snowproof import database, preparation  # noqa: E402


def main() -> None:
    """
    Coverage check, cleaning, and the weekly labels (good week: 1, 0 or unknown).

    Owner:    Nico + Julian (Task 4 and Task 6)
    Used by:  run by hand
    Returns:  nothing
    """
    # TODO [NICO+JULIAN | Task 4] Prepare the labels
    # Step 1: snow = database.load_table("snow_daily").
    # Step 2: coverage = preparation.check_station_coverage(snow). Print it and save it as a CSV for the team.
    #         DISCUSS with Julian: which years can we train on? Update ml/evaluate.py if needed.
    # Step 3: clean = preparation.clean_snow_daily(snow).
    # Step 4: labels = preparation.label_good_weeks(clean) -> database.save_table(labels, "weekly_labels").
    # Step 5: Print the share of 1, 0 and unknown labels.
    # Done when: tests/test_labels.py passes and weekly_labels has rows for every station.
    raise NotImplementedError("TODO [NICO+JULIAN | Task 4]: 03_prepare_labels.main")


if __name__ == "__main__":
    main()
