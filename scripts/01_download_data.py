"""
01_download_data.py: download everything we need, once. STEP 1 OF 5.

Owner:       Nico (Task 3 and 5), Jan for holidays and transport stops (Task 8)
Depends on:  snowproof/data_sources/*.py, snowproof/database.py (fetch_with_cache)
Used by:     run by hand: python scripts/01_download_data.py
Flow:        Step 1 of 5. Next: 02_build_database.py

Run it from the repository root. Thanks to fetch_with_cache, a second run is fast and offline.
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # so "import snowproof" works

from snowproof import config, database  # noqa: E402
from snowproof.data_sources import holidays, meteoswiss, open_meteo, overpass, transport  # noqa: E402


def main() -> None:
    """
    Download stations, snow depth, weather, resorts, pistes, lifts, stops and holidays.

    Owner:    Nico (Task 3 and 5), Jan (Task 8)
    Used by:  run by hand
    Returns:  nothing (everything ends up in config.RAW_DIR and the database)
    """
    # TODO [NICO | Task 3] Download step by step
    # Step 1: stations = meteoswiss.list_stations(). Print how many you got.
    # Step 2: For each station: database.fetch_with_cache(f"snow_{code}", meteoswiss.fetch_snow_depth,
    #         code, date(1930, 1, 1), date.today()). Then database.save_snow_daily(...).
    # Step 3: Same idea for open_meteo.fetch_weather (from 1950, ERA5 starts there).
    # Step 4: resorts, pistes and lifts from overpass (cached), then overpass.compute_piste_km.
    # Hint:   Start with 3 stations (DAV, WFJ and one low station) until everything works. Then run all.
    # Hint:   Print progress ("12 of 85 stations done"), downloads take a while.
    # Done when: config.RAW_DIR contains files and a second run finishes in seconds.
    # TODO [JAN | Task 8] Add holidays and transport stops here
    # Step 1: holidays.fetch_school_holidays for the coming winter -> database.save_table(..., "holiday_periods").
    # Step 2: For each resort: transport.find_nearest_stop(lat, lon) -> database.save_table(..., "transport_stops").
    # Done when: both tables have rows.
    raise NotImplementedError("TODO [NICO | Task 3]: 01_download_data.main")


if __name__ == "__main__":
    main()
