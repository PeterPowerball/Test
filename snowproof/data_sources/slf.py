"""
slf.py: OPTIONAL second snow source (SLF / IMIS stations).

Owner:       Nico (Task 3, optional, only if time allows)
Depends on:  config.py
Used by:     nobody yet
Flow:        Step 1 of 5 (download data), optional

Why? MeteoSwiss has few stations high up in ski areas. SLF stations are higher,
but their records are much shorter. Only add this if the coverage check shows a real gap.
"""

from datetime import date

import pandas as pd


def fetch_slf_snow_depth(station_code: str, start: date, end: date) -> pd.DataFrame:
    """
    Daily snow depth from one SLF station. OPTIONAL.

    Owner:    Nico (Task 3, optional)
    Used by:  (optional) scripts/01_download_data.py
    Source:   SLF measurement data (check the SLF data portal for the current download options)
    Returns:  same columns as meteoswiss.fetch_snow_depth():
                station_code (str), date (datetime.date), snow_depth_cm (float), new_snow_cm (float)
    """
    # TODO [NICO | Task 3, optional] Second snow source from SLF
    # Step 1: Ask the team first: does the coverage check (preparation.check_station_coverage) show
    #         resorts without any good MeteoSwiss station? If not, skip this file.
    # Step 2: Find how SLF offers its station data and the license terms.
    # Step 3: Return exactly the same columns as fetch_snow_depth, so nothing else has to change.
    # Hint:   SLF records usually start in the 1990s, too short for the 1950 to 2025 validation.
    # Done when: the team decided to use it, and the columns match fetch_snow_depth.
    raise NotImplementedError("TODO [NICO | Task 3, optional]: fetch_slf_snow_depth")
