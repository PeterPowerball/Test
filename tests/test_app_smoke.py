"""Smoke tests: every page loads without errors, plus the main user flows.

Run with:  pytest
"""

import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from streamlit.testing.v1 import AppTest  # noqa: E402

from snowproof import config, data_access  # noqa: E402


def run_page(path: str, **state) -> AppTest:
    """Load a page with some session state preset and run it."""
    at = AppTest.from_file(str(ROOT / path), default_timeout=60)
    for key, value in state.items():
        at.session_state[key] = value
    return at.run()


def texts(at: AppTest) -> str:
    """All visible text of the app in one string, to search in."""
    parts = [m.value for m in at.markdown] + [w.value for w in at.warning]
    parts += [i.value for i in at.info] + [s.value for s in at.success] + [c.value for c in at.caption]
    return "\n".join(parts)


# ------------------------------------------------------------------ every page loads
def test_entry_point_loads():
    at = AppTest.from_file(str(ROOT / "streamlit_app.py"), default_timeout=60).run()
    assert not at.exception


def test_explore_page_empty_state():
    at = run_page("pages/explore.py")
    assert not at.exception
    assert "Click a resort on the map" in texts(at)
    assert not at.metric  # no resort panel yet, the map uses the full width
    assert "24 of 24 resorts match" in texts(at)


def test_model_page_loads():
    assert not run_page("pages/model.py").exception


def test_future_page_loads():
    at = run_page("pages/future.py")
    assert not at.exception
    assert "Coming later" in texts(at)


# ------------------------------------------------------------------- main user flows
def test_selecting_a_resort_shows_the_panel():
    at = run_page("pages/explore.py", selected_resort_id="davos")
    assert not at.exception
    assert "Davos" in texts(at) and "Davos Klosters" in "".join(s.value for s in at.subheader)
    assert sorted(m.label for m in at.metric) == ["Base altitude", "Lifts", "Piste km", "Summit altitude"]
    assert "Snow data from station **Davos**" in texts(at)


def test_opening_the_snow_check():
    at = run_page("pages/explore.py", selected_resort_id="davos", view="snow",
                  check_range=(date(2027, 2, 13), date(2027, 2, 19)))
    assert not at.exception
    assert "chance of a good ski week" in texts(at)
    assert "at least 50 cm" in texts(at)
    assert "Historical average for this week" in texts(at)


def test_snow_check_with_several_weeks():
    at = run_page("pages/explore.py", selected_resort_id="soerenberg", view="snow",
                  check_range=(date(2027, 2, 6), date(2027, 2, 25)))
    assert not at.exception
    assert "chance of a good ski week" in texts(at)


def test_closing_the_resort_panel():
    at = run_page("pages/explore.py", selected_resort_id="davos")
    [b for b in at.button if b.label == "Close"][0].click().run()
    assert not at.exception
    assert at.session_state["selected_resort_id"] is None
    assert not at.metric


def test_resort_without_station_disables_the_button():
    at = run_page("pages/explore.py", selected_resort_id="flumserberg")
    assert not at.exception
    assert "No reliable measurement station nearby" in texts(at)
    check = [b for b in at.button if b.label == "Check the snow for your holiday"][0]
    assert check.disabled


def test_dates_outside_the_season_show_a_friendly_message():
    at = run_page("pages/explore.py", selected_resort_id="davos", view="snow",
                  check_range=(date(2027, 7, 10), date(2027, 7, 16)))
    assert not at.exception
    assert "December to April" in texts(at)


def test_filters_that_match_nothing():
    # Geneva is more than an hour from every resort in the mock data, so nothing matches
    at = run_page("pages/explore.py", home_address="Geneva", max_hours=1.0)
    assert not at.exception
    assert "0 of 24 resorts match" in texts(at)
    assert "No resort matches your filters" in texts(at)


def test_holiday_dates_in_sidebar_show_a_ranking():
    at = run_page("pages/explore.py", holiday_range=(date(2027, 2, 13), date(2027, 2, 19)))
    assert not at.exception
    assert "Best resorts for your dates" in "".join(s.value for s in at.subheader)


def test_holiday_dates_outside_season_in_sidebar():
    at = run_page("pages/explore.py", holiday_range=(date(2027, 6, 1), date(2027, 6, 7)))
    assert not at.exception
    assert "December to April" in texts(at)


# ----------------------------------------------------------------- data layer checks
def test_mock_data_is_deterministic():
    a = data_access.predict_good_week("davos", date(2027, 2, 13), date(2027, 2, 19))
    b = data_access.predict_good_week("davos", date(2027, 2, 13), date(2027, 2, 19))
    assert a["chance"] == b["chance"]
    assert 0 <= a["chance"] <= 1


def test_altitude_and_season_make_sense():
    high = data_access.predict_good_week("saasfee", date(2027, 2, 6), date(2027, 2, 12))["chance"]
    low = data_access.predict_good_week("pizol", date(2027, 2, 6), date(2027, 2, 12))["chance"]
    december = data_access.predict_good_week("davos", date(2026, 12, 5), date(2026, 12, 11))["chance"]
    february = data_access.predict_good_week("davos", date(2027, 2, 6), date(2027, 2, 12))["chance"]
    assert high > low
    assert february > december


def test_between_three_and_four_resorts_have_no_station():
    resorts = data_access.get_resorts()
    assert 20 <= len(resorts) <= 25
    assert 3 <= (~resorts["has_station"]).sum() <= 4
    assert data_access.get_linked_station("stoos") is None


def test_validation_rejects_bad_dates():
    assert config.validate_holiday_range(date(2027, 2, 1), date(2027, 1, 1))
    assert config.validate_holiday_range(date(2027, 7, 1), date(2027, 7, 7))
    assert config.validate_holiday_range(date(2027, 2, 1), date(2027, 2, 7)) is None
