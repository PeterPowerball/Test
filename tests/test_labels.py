"""
test_labels.py: test cases for the 7-day rule (data.label_good_weeks).

Owner:       Nico + Julian (Task 4 and Task 6)
Depends on:  snowproof/data.py
Used by:     "pytest"
Flow:        Step 3 of 5. Write these tests BEFORE (or while) you write label_good_weeks.

Every test is skipped for now. To build a test: create a tiny DataFrame by hand (one station,
7 or more days, columns station_code, date, snow_depth_cm, new_snow_cm), run
label_good_weeks on it, and check good_week. Then delete the pytest.skip line.

The rule: good_week = 1 if snow_depth_cm >= 50 on all 7 days,
          0 if at least one day is below 50,
          unknown (NaN) if a day is missing and no day is below 50.
"""

import pytest

from snowproof import data  # noqa: F401  (used once the tests are written)


def test_seven_days_above_threshold_is_good_week():
    # TODO [NICO+JULIAN | Task 4] 7 days with 60 cm each -> good_week == 1
    pytest.skip("TODO [NICO+JULIAN | Task 4]: write this test")


def test_exactly_50_cm_counts_as_good():
    # TODO [NICO+JULIAN | Task 4] 7 days with exactly 50 cm -> good_week == 1 (50 is included, ">=")
    pytest.skip("TODO [NICO+JULIAN | Task 4]: write this test")


def test_one_day_below_threshold_is_bad_week():
    # TODO [NICO+JULIAN | Task 4] 6 days with 80 cm and one day with 49 cm -> good_week == 0
    pytest.skip("TODO [NICO+JULIAN | Task 4]: write this test")


def test_missing_day_makes_week_unknown():
    # TODO [NICO+JULIAN | Task 4] 6 days with 80 cm and one day NaN -> good_week is NaN (not 0!)
    pytest.skip("TODO [NICO+JULIAN | Task 4]: write this test")


def test_missing_day_and_low_day_is_bad_week():
    # TODO [NICO+JULIAN | Task 4] one day NaN and one day 20 cm -> good_week == 0
    #      (the low day already decides it, the missing day does not matter)
    pytest.skip("TODO [NICO+JULIAN | Task 4]: write this test")


def test_zero_snow_is_not_the_same_as_missing():
    # TODO [NICO+JULIAN | Task 4] a day with 0 cm -> good_week == 0, a day with NaN -> unknown
    pytest.skip("TODO [NICO+JULIAN | Task 4]: write this test")


def test_fewer_than_seven_days_gives_no_label():
    # TODO [NICO+JULIAN | Task 4] only 5 days of data -> no row (or unknown), never a 1
    pytest.skip("TODO [NICO+JULIAN | Task 4]: write this test")


def test_weeks_across_new_year_have_correct_season_year():
    # TODO [NICO+JULIAN | Task 4] a week from 28 Dec 2019 to 3 Jan 2020 -> season_year == 2020
    #      (the whole winter 2019/20 belongs to season_year 2020)
    pytest.skip("TODO [NICO+JULIAN | Task 4]: write this test")


def test_only_season_months_are_labelled():
    # TODO [NICO+JULIAN | Task 4] a week in July -> no row in the result
    pytest.skip("TODO [NICO+JULIAN | Task 4]: write this test")


def test_stations_are_labelled_separately():
    # TODO [NICO+JULIAN | Task 4] two stations in one DataFrame -> a window never mixes days of both stations
    pytest.skip("TODO [NICO+JULIAN | Task 4]: write this test")
