"""
test_app_smoke.py: the app starts and every page loads without errors.

Owner:       Fabio (Task 12: integration and testing)
Depends on:  streamlit_app.py, pages/*.py
Used by:     "pytest" (run it before every pull request)
Flow:        testing, all the time

A 🚧 box is fine. An exception (red error box) is not.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pytest  # noqa: E402
from streamlit.testing.v1 import AppTest  # noqa: E402

from snowproof import config, data_access  # noqa: E402

PAGES = ["pages/explore.py", "pages/model.py", "pages/about.py", "pages/future.py"]


def test_entry_point_starts():
    at = AppTest.from_file(str(ROOT / "streamlit_app.py"), default_timeout=60).run()
    assert not at.exception


@pytest.mark.parametrize("page", PAGES)
def test_page_loads_without_errors(page):
    at = AppTest.from_file(str(ROOT / page), default_timeout=60).run()
    assert not at.exception, f"{page} raised: {[e.value for e in at.exception]}"


def test_mock_data_is_on_while_building():
    # The skeleton must run on mock data until the real pipeline is finished (Task 12 switches it off)
    assert config.USE_MOCK_DATA is True
    assert len(data_access.get_resorts()) > 0
