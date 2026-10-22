"""
02_build_database.py: create the SQLite tables and fill them. STEP 2 OF 5.

Owner:       Nico (Task 4: database and data preparation)
Depends on:  snowproof/database.py, snowproof/preparation.py, the downloads from step 1
Used by:     run by hand: python scripts/02_build_database.py
Flow:        Step 2 of 5. Before: 01_download_data.py. Next: 03_prepare_labels.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from snowproof import database, preparation  # noqa: E402


def main() -> None:
    """
    Create all tables, save the downloaded data, and link stations to resorts.

    Owner:    Nico (Task 4: database and data preparation)
    Used by:  run by hand
    Returns:  nothing
    """
    # TODO [NICO | Task 4] Build the database
    # Step 1: database.create_tables().
    # Step 2: Save stations, resorts, pistes (with resort_id), weather into their tables (database.save_table).
    # Step 3: Per resort: piste km per difficulty, number of lifts, base and summit altitude
    #         (swisstopo.get_altitude for the lowest and highest piste point). Update the resorts table.
    # Step 4: mapping = preparation.map_stations_to_resorts(resorts, stations) -> "resort_station_mapping".
    # Step 5: Print a short summary: number of rows per table.
    # Done when: the summary shows rows in stations, resorts, snow_daily, pistes and resort_station_mapping.
    raise NotImplementedError("TODO [NICO | Task 4]: 02_build_database.main")


if __name__ == "__main__":
    main()
