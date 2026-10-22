"""
config.py: all constants in one place (colors, snow rule, file paths, API URLs, switches).

Owner:       Fabio (Task 2: technical foundation). Everyone may ADD constants, but tell the team.
Depends on:  nothing
Used by:     almost every file
Flow:        foundation, used in all steps (1 to 5) and by the app

Why one file? If the snow threshold or a URL changes, we change it here once,
and every script, model and page uses the new value automatically.
"""

from pathlib import Path

# ============================================================================
# Switches
# ============================================================================
# True:  data_access.py returns mock data, so the UI can be built before the real data exists.
# False: data_access.py reads from our SQLite database and the trained model.
# Fabio switches this to False during integration (Task 12), when steps 1 to 5 are done.
USE_MOCK_DATA = True

# The Future outlook page (Use Case 2) is optional. It only shows in the navigation when True.
SHOW_FUTURE_PAGE = False

# ============================================================================
# The snow rule (our target variable)
# ============================================================================
GOOD_SNOW_CM = 50                   # minimum measured snow depth on EVERY day of the week
GOOD_WEEK_DAYS = 7                  # a "week" has 7 consecutive days
SEASON_MONTHS = (12, 1, 2, 3, 4)    # December to April
MAX_STAY_DAYS = 28                  # longest stay the snow check accepts

# ============================================================================
# File paths (relative to the repository root, so they work locally and on Streamlit Cloud)
# ============================================================================
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"                 # downloads and the database (gitignored)
RAW_DIR = DATA_DIR / "raw"                   # cached raw downloads (see database.fetch_with_cache)
DB_PATH = DATA_DIR / "snowproof.sqlite"      # our SQLite database
MODELS_DIR = ROOT_DIR / "models"
MODEL_PATH = MODELS_DIR / "good_week_model.joblib"

# ============================================================================
# API base URLs (all free, no API key needed)
# ============================================================================
# MeteoSwiss Open Data (measured snow depth = our training target)
METEOSWISS_STAC_URL = "https://data.geo.admin.ch/api/stac/v1"
METEOSWISS_COLLECTION = "ch.meteoschweiz.ogd-nime"
METEOSWISS_SNOW_DEPTH_COLUMN = "hto000d0"    # total snow depth, daily, cm
METEOSWISS_NEW_SNOW_COLUMN = "hns000d0"      # new snow, daily, cm

# Open-Meteo Historical Weather (ERA5 reanalysis, from 1950). Only used for FEATURES, never the target.
OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
OPEN_METEO_DAILY_VARIABLES = ["temperature_2m_mean", "snowfall_sum", "precipitation_sum"]

# OpenStreetMap Overpass (resorts, pistes, lifts). The Swiss instance, because overpass-api.de hung in our tests.
OVERPASS_URL = "https://overpass.osm.ch/api/interpreter"
OSM_ATTRIBUTION = "© OpenStreetMap contributors"

# swisstopo / geo.admin.ch (address search and altitude)
SWISSTOPO_SEARCH_URL = "https://api3.geo.admin.ch/rest/services/api/SearchServer"
SWISSTOPO_HEIGHT_URL = "https://api3.geo.admin.ch/rest/services/height"

# Public transport (travel time)
TRANSPORT_BASE_URL = "https://transport.opendata.ch/v1"

# School holidays
OPENHOLIDAYS_URL = "https://openholidaysapi.org"

# Polite defaults for every web request
REQUEST_TIMEOUT_SECONDS = 60
USER_AGENT = "Snow-Proof student project (University of St. Gallen)"

# ============================================================================
# Model and validation
# ============================================================================
RANDOM_SEED = 42      # so model results are the same on every run
# The walk-forward rounds live in snowproof/ml/evaluate.py (WALK_FORWARD_ROUNDS).

# ============================================================================
# Map
# ============================================================================
MAP_CENTER = (46.85, 8.2)
MAP_ZOOM = 8
SWISSTOPO_TILES = (
    "https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/{z}/{x}/{y}.jpeg"
)
SWISSTOPO_ATTRIBUTION = "© swisstopo"
MAX_TRAVEL_HOURS = 8.0

# ============================================================================
# Colors (same as the prototype on the ui-prototype branch)
# ============================================================================
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
