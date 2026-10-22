"""
holidays.py: school holidays per canton (OpenHolidays API).

Owner:       Jan (Task 8: location, travel and holiday filters)
Depends on:  config.py
Used by:     scripts/01_download_data.py
Flow:        Step 1 of 5 (download data)
"""

from datetime import date

import pandas as pd
import requests

from snowproof import config


def fetch_school_holidays(valid_from: date, valid_to: date) -> pd.DataFrame:
    """
    School holiday periods of all Swiss cantons between two dates.

    Owner:    Jan (Task 8: location, travel and holiday filters)
    Used by:  scripts/01_download_data.py -> database.save_table(..., "holiday_periods")
    Source:   OpenHolidays API /SchoolHolidays, config.OPENHOLIDAYS_URL
    Returns:  DataFrame with columns
                canton (str, e.g. "ZH"), holiday_name (str, e.g. "Sportferien"),
                start_date (datetime.date), end_date (datetime.date)
    """
    # TODO [JAN | Task 8] Download school holidays
    # Step 1: Call f"{config.OPENHOLIDAYS_URL}/SchoolHolidays" with params countryIsoCode="CH",
    #         languageIsoCode="EN", validFrom="YYYY-MM-DD", validTo="YYYY-MM-DD".
    # Step 2: Each entry has "subdivisions" with codes like "CH-ZH". Turn them into canton codes.
    # Step 3: Keep only periods that touch the ski season (config.SEASON_MONTHS).
    # Hint:   Sportferien are often missing or differ by municipality. The user must ALWAYS be able
    #         to pick dates manually. This helper only suggests dates.
    # Hint:   The API allows at most about 3 years per request.
    # Done when: the result has rows for ZH and BE with Christmas holidays.
    raise NotImplementedError("TODO [JAN | Task 8]: fetch_school_holidays")
