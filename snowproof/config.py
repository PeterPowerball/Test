"""Central place for colors and constants, so every page looks and behaves the same.

If you want to change a color or the snow threshold, do it here and only here.
"""

from datetime import date, timedelta

# ---------------------------------------------------------------- brand colors
BRAND_BLUE = "#0B3C6F"   # deep blue, main color
ACCENT_BLUE = "#2E86C1"  # lighter blue for secondary elements
ICE_BLUE = "#D9ECF8"     # very light blue for backgrounds
GREY = "#9AA5B1"         # neutral grey (also: resorts without a station)
TEXT_DARK = "#14213D"

# Traffic light scale for the chance of a good ski week
GREEN = "#2E9E5B"
AMBER = "#F2A900"
RED = "#D64545"
GOOD_CHANCE_MIN = 0.60   # at or above: green
OK_CHANCE_MIN = 0.30     # at or above: amber, below: red

# Swiss piste difficulty colors
PISTE_COLORS = {"Blue (easy)": "#1F77D0", "Red (medium)": "#D62828", "Black (difficult)": "#222222"}

# ------------------------------------------------------------- snow definition
GOOD_SNOW_CM = 50          # minimum snow depth on every day of the week
GOOD_WEEK_DAYS = 7         # a "week" has 7 days
SEASON_MONTHS = (12, 1, 2, 3, 4)   # December to April
MAX_STAY_DAYS = 28         # keeps the weekly table short and readable

# ------------------------------------------------------------------------ map
MAP_CENTER = (46.85, 8.2)
MAP_ZOOM = 8
SWISSTOPO_TILES = (
    "https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/{z}/{x}/{y}.jpeg"
)
SWISSTOPO_ATTRIBUTION = "© swisstopo"

# Travel time slider (hours)
MAX_TRAVEL_HOURS = 8.0


def chance_color(chance: float) -> str:
    """Return the traffic light color for a chance between 0 and 1."""
    if chance >= GOOD_CHANCE_MIN:
        return GREEN
    if chance >= OK_CHANCE_MIN:
        return AMBER
    return RED


def chance_label(chance: float) -> str:
    """Return a short verdict matching the traffic light color."""
    if chance >= GOOD_CHANCE_MIN:
        return "Good odds"
    if chance >= OK_CHANCE_MIN:
        return "Mixed odds"
    return "Poor odds"


def default_trip_dates() -> tuple[date, date]:
    """Next mid-February week, used to pre-fill the snow check when no dates are set."""
    today = date.today()
    start = date(today.year, 2, 13)
    if start < today:
        start = date(today.year + 1, 2, 13)
    return start, start + timedelta(days=GOOD_WEEK_DAYS - 1)


def validate_holiday_range(start: date, end: date) -> str | None:
    """Return a friendly error message if the dates are not usable, else None."""
    if end < start:
        return "The end date is before the start date."
    if (end - start).days + 1 > MAX_STAY_DAYS:
        return f"Please pick at most {MAX_STAY_DAYS} days."
    day = start
    while day <= end:
        if day.month not in SEASON_MONTHS:
            return "Snow-Proof covers the ski season from December to April. Please pick dates in that period."
        day += timedelta(days=1)
    return None
