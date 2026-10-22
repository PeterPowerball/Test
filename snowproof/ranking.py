"""
ranking.py: rank resorts by their chance of a good ski week.

Owner:       Jan (Task 9: resort ranking)
Depends on:  data_access.py (predictions and travel times)
Used by:     data_access.get_ranked_resorts(), pages/explore.py (ranked list, map colors)
Flow:        app (runs live when the user sets holiday dates)
"""

from datetime import date

import pandas as pd


def rank_resorts(predictions: pd.DataFrame) -> pd.DataFrame:
    """
    Sort resorts from best to worst chance.

    Owner:    Jan (Task 9: resort ranking)
    Used by:  data_access.get_ranked_resorts()
    Source:   one row per resort with columns resort_id, name, canton, chance, baseline, travel_minutes
    Returns:  the same columns, sorted by chance (best first), resorts without a station removed,
              plus a column rank (int, 1 = best)
    """
    # TODO [JAN | Task 9] Rank resorts
    # Step 1: Drop rows where chance is missing (resorts without a reliable station).
    # Step 2: Sort by chance, highest first (DataFrame.sort_values).
    # Step 3: Add the rank column and reset the index.
    # Hint:   Think about ties: with equal chance, should the shorter travel time win? Decide as a team.
    # Done when: the first row has the highest chance and rank 1.
    raise NotImplementedError("TODO [JAN | Task 9]: rank_resorts")


def find_similar_resorts(resort_id: str, start_date: date, end_date: date,
                         place: str = "", count: int = 3) -> pd.DataFrame:
    """
    OPTIONAL: other resorts with a better chance and a similar travel time.

    Owner:    Jan (Task 9, optional)
    Used by:  pages/explore.py (optional "Similar resorts with better chances" section)
    Source:   data_access.get_ranked_resorts(), data_access.get_travel_time_minutes()
    Returns:  same columns as rank_resorts(), at most `count` rows
    """
    # TODO [JAN | Task 9, optional] Similar resorts with better chances
    # Step 1: Rank all other resorts for the same dates.
    # Step 2: Keep those with a clearly higher chance (e.g. at least 2 points more).
    # Step 3: "Similar": within 60 minutes of this resort's travel time, or within 150 km if no place is set.
    # Hint:   This section was removed from the prototype after feedback. Only build it if the team wants it.
    # Done when: a low resort in December gets higher alternatives nearby.
    raise NotImplementedError("TODO [JAN | Task 9, optional]: find_similar_resorts")
