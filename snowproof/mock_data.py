"""
mock_data.py: fake data for the UI, so Noah can build every page before the real data exists.

Owner:       nobody needs to change this file. It comes from the clickable prototype.
Depends on:  config.py
Used by:     data_access.py, but only while config.USE_MOCK_DATA is True
Flow:        not part of the real pipeline. Delete it at the very end, once the real data works.

EVERYTHING in this file is a placeholder. Numbers are approximate or invented.
The functions at the bottom (get_resorts, predict_good_week, ...) have the same names and
return the same columns as data_access.py. They are the contract for the real versions.
All "random" values are seeded by the resort id, so they stay the same on every rerun.
"""

import math
import random
from datetime import date, timedelta

import pandas as pd

from snowproof import config

# ----------------------------------------------------------------------------
# Resorts. PLACEHOLDER values (approximate coordinates, altitudes, piste km).
# Columns: id, name, canton, lat, lon, base m, summit m, blue km, red km,
#          black km, lifts, description, station (name, altitude m, distance km)
# A station of None means "no reliable measurement station nearby".
# ----------------------------------------------------------------------------
_RESORTS = [
    ("zermatt", "Zermatt", "VS", 46.02, 7.75, 1620, 3883, 130, 170, 60, 52,
     "Car-free village below the Matterhorn with year-round glacier skiing.", ("Zermatt", 1638, 1.0)),
    ("verbier", "Verbier", "VS", 46.10, 7.23, 1500, 3330, 140, 200, 70, 65,
     "Large freeride playground in the Four Valleys.", ("Verbier", 1530, 1.5)),
    ("davos", "Davos Klosters", "GR", 46.80, 9.84, 1560, 2844, 110, 140, 50, 53,
     "Classic Grisons ski region with several mountains and long runs.", ("Davos", 1594, 3.0)),
    ("stmoritz", "St. Moritz", "GR", 46.50, 9.82, 1720, 3303, 100, 130, 40, 24,
     "Sunny Engadin resort with glamorous après-ski and high slopes.", ("Samedan", 1708, 5.0)),
    ("laax", "Laax", "GR", 46.84, 9.26, 1100, 3018, 90, 120, 40, 28,
     "Snow parks and a glacier-fed top section above Flims and Laax.", ("Flims", 1100, 4.0)),
    ("engelberg", "Engelberg-Titlis", "OW", 46.82, 8.41, 1000, 3020, 30, 50, 25, 26,
     "Central Switzerland with the Titlis glacier and famous off-piste.", ("Engelberg", 1035, 1.0)),
    ("saasfee", "Saas-Fee", "VS", 46.11, 7.93, 1800, 3600, 40, 60, 25, 22,
     "Car-free glacier village, very snow-reliable.", ("Saas-Fee", 1830, 1.0)),
    ("arosa", "Arosa Lenzerheide", "GR", 46.78, 9.68, 1230, 2865, 80, 110, 40, 43,
     "Two villages joined by a gondola, family friendly.", ("Arosa", 1878, 2.0)),
    ("adelboden", "Adelboden-Lenk", "BE", 46.49, 7.56, 1350, 2362, 60, 85, 35, 53,
     "Bernese Oberland ski area known for its World Cup slope.", ("Adelboden", 1320, 1.0)),
    ("grindelwald", "Grindelwald-Wengen", "BE", 46.62, 8.04, 1034, 2500, 60, 90, 30, 28,
     "Below the Eiger north face with the long Lauberhorn run.", ("Grindelwald", 1034, 1.0)),
    ("andermatt", "Andermatt-Sedrun", "UR", 46.63, 8.59, 1444, 2961, 50, 70, 35, 27,
     "Alpine pass region with a lot of natural snow.", ("Andermatt", 1442, 1.0)),
    ("flumserberg", "Flumserberg", "SG", 47.11, 9.28, 1220, 2222, 25, 35, 10, 17,
     "Family resort above the Walensee, close to Zurich.", None),
    ("cransmontana", "Crans-Montana", "VS", 46.31, 7.48, 1500, 3000, 55, 70, 25, 25,
     "Sunny plateau with views of the Valais Alps.", ("Montana", 1500, 2.0)),
    ("gstaad", "Gstaad", "BE", 46.47, 7.29, 1000, 3000, 80, 95, 30, 40,
     "Elegant Saanenland ski area including the Glacier 3000.", ("Gstaad", 1050, 1.5)),
    ("pizol", "Pizol", "SG", 46.96, 9.40, 840, 2227, 20, 25, 10, 10,
     "Smaller ski area in eastern Switzerland with low base.", ("Bad Ragaz", 500, 8.0)),
    ("hochybrig", "Hoch-Ybrig", "SZ", 47.03, 8.78, 1050, 1850, 15, 20, 5, 9,
     "Low, small resort with a quick access from Zurich.", None),
    ("soerenberg", "Sörenberg", "LU", 46.82, 8.03, 1166, 2350, 20, 25, 8, 10,
     "Entlebuch biosphere ski area, small and quiet.", ("Sörenberg", 1165, 0.5)),
    ("villars", "Villars", "VD", 46.30, 7.05, 1253, 2120, 40, 55, 15, 25,
     "Vaudois Alps resort with a view of Lake Geneva.", ("Villars", 1260, 0.5)),
    ("leukerbad", "Leukerbad", "VS", 46.38, 7.63, 1411, 2610, 20, 30, 10, 8,
     "Thermal spa village with a compact ski area.", ("Leukerbad", 1411, 0.5)),
    ("elm", "Elm", "GL", 46.92, 9.17, 1000, 2105, 10, 18, 8, 7,
     "Quiet Glarus valley, popular with ski tourers.", ("Elm", 960, 0.5)),
    ("braunwald", "Braunwald", "GL", 46.94, 8.99, 1256, 1900, 10, 15, 5, 6,
     "Car-free terrace village with a small family ski area.", None),
    ("hasliberg", "Meiringen-Hasliberg", "BE", 46.75, 8.20, 1050, 2433, 30, 40, 15, 11,
     "Sunny terrace above the Haslital with a broad family area.", ("Meiringen", 595, 6.0)),
    ("diablerets", "Les Diablerets", "VD", 46.35, 7.20, 1100, 3000, 35, 45, 20, 14,
     "Glacier 3000 gives a snow-sure top section above a low village.", ("Les Diablerets", 1155, 1.0)),
    ("stoos", "Stoos", "SZ", 46.98, 8.66, 1300, 1922, 12, 18, 5, 6,
     "Car-free village reached by the steepest funicular in the world.", None),
]

_CITIES = {
    # name or alias: (lat, lon) - used for mock travel times
    "zurich": (47.378, 8.540), "zürich": (47.378, 8.540), "bern": (46.949, 7.439),
    "basel": (47.548, 7.590), "geneva": (46.210, 6.142), "genf": (46.210, 6.142),
    "lausanne": (46.520, 6.633), "st. gallen": (47.424, 9.377), "st gallen": (47.424, 9.377),
    "lucerne": (47.050, 8.310), "luzern": (47.050, 8.310), "lugano": (46.004, 8.951),
    "chur": (46.850, 9.532), "winterthur": (47.500, 8.724), "sion": (46.233, 7.360),
}

# Mock school holidays for the 2026/27 season (PLACEHOLDERS, not official dates).
_CANTONS = ["AG", "AI", "AR", "BE", "BL", "BS", "FR", "GE", "GL", "GR", "JU", "LU", "NE",
            "NW", "OW", "SG", "SH", "SO", "SZ", "TG", "TI", "UR", "VD", "VS", "ZG", "ZH"]
_CHRISTMAS = (date(2026, 12, 19), date(2027, 1, 3))
_EASTER = (date(2027, 3, 27), date(2027, 4, 11))
_SPORT = {  # canton -> mock Sportferien
    "BE": (date(2027, 2, 6), date(2027, 2, 21)), "GR": (date(2027, 2, 13), date(2027, 2, 28)),
    "VS": (date(2027, 2, 13), date(2027, 2, 28)), "VD": (date(2027, 2, 13), date(2027, 2, 28)),
    "GE": (date(2027, 2, 13), date(2027, 2, 21)), "ZH": (date(2027, 2, 6), date(2027, 2, 21)),
}
_SPORT_DEFAULT = (date(2027, 2, 6), date(2027, 2, 21))


# ----------------------------------------------------------------------------
# Tables
# ----------------------------------------------------------------------------
def resorts_table() -> pd.DataFrame:
    """One row per resort, with piste km split by difficulty and station info."""
    rows = []
    for (rid, name, canton, lat, lon, base, summit, blue, red, black, lifts, desc, station) in _RESORTS:
        rows.append({
            "resort_id": rid, "name": name, "canton": canton, "lat": lat, "lon": lon,
            "base_altitude_m": base, "summit_altitude_m": summit,
            "piste_blue_km": blue, "piste_red_km": red, "piste_black_km": black,
            "total_piste_km": blue + red + black, "lifts": lifts, "description": desc,
            "station_name": station[0] if station else None,
            "station_altitude_m": station[1] if station else None,
            "station_distance_km": station[2] if station else None,
            "has_station": station is not None,
        })
    return pd.DataFrame(rows)


def cantons() -> list[str]:
    """All 26 cantons (needed for the school holiday helper)."""
    return list(_CANTONS)


def school_holidays(canton: str) -> list[tuple[date, date]]:
    """Mock holiday periods: Christmas, Sportferien (varies by canton), Easter."""
    return [_CHRISTMAS, _SPORT.get(canton, _SPORT_DEFAULT), _EASTER]


# ----------------------------------------------------------------------------
# Travel time (straight line distance to a few hard-coded cities)
# ----------------------------------------------------------------------------
def _distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Straight-line distance on the earth (haversine formula)."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(a))


def travel_minutes(home_address: str, lat: float, lon: float) -> int | None:
    """Mock: find a known city in the address and turn the distance into minutes."""
    text = (home_address or "").lower()
    for city, (clat, clon) in _CITIES.items():
        if city in text:
            km = _distance_km(clat, clon, lat, lon)
            return int(km * 1.4 + 30)  # winding mountain roads plus changing trains
    return None


# ----------------------------------------------------------------------------
# Snow model (mock). A smooth formula that looks plausible, nothing more.
# ----------------------------------------------------------------------------
def resort_factor(resort_id: str) -> float:
    """Fixed +-10% 'personality' of a resort, seeded by its id."""
    return random.Random(resort_id).uniform(0.9, 1.1)


def snow_altitude(row) -> float:
    """Altitude used for the snow formula: the station if there is one, else the resort middle."""
    if row["has_station"]:
        return float(row["station_altitude_m"])
    return (row["base_altitude_m"] + row["summit_altitude_m"]) / 2


def expected_depth_cm(altitude_m: float, day: date, factor: float = 1.0, shift_m: float = 0.0) -> float:
    """Expected snow depth: higher up means more snow, peak around 1 February."""
    peak = min(max((altitude_m + shift_m - 950) * 0.16, 0.0), 260.0) * factor
    season_year = day.year + 1 if day.month >= 7 else day.year
    days_from_peak = (day - date(season_year, 2, 1)).days
    return peak * math.exp(-0.5 * (days_from_peak / 42) ** 2)


def _spread_cm(depth: float) -> float:
    """Uncertainty (one standard deviation) grows with the depth."""
    return 8 + 0.22 * depth


def _normal_cdf(z: float) -> float:
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def week_chance(altitude_m: float, days: list[date], factor: float = 1.0, shift_m: float = 0.0) -> float:
    """Chance that all days reach the snow threshold (driven by the weakest day)."""
    weakest = min(expected_depth_cm(altitude_m, d, factor, shift_m) for d in days)
    z = (weakest * 0.97 - config.GOOD_SNOW_CM) / _spread_cm(weakest)
    return min(max(_normal_cdf(z), 0.01), 0.99)


def split_into_weeks(start: date, end: date) -> list[list[date]]:
    """Cut the stay into blocks of 7 days (the last block may be shorter)."""
    days = [start + timedelta(days=i) for i in range((end - start).days + 1)]
    return [days[i:i + config.GOOD_WEEK_DAYS] for i in range(0, len(days), config.GOOD_WEEK_DAYS)]


def decade_shift_m(decade: int) -> float:
    """Past decades were colder: the snow behaves as if the resort were higher up."""
    return (2025 - (decade + 5)) * 2.5


def historical_share(row, calendar_week: int, decade: int) -> float:
    """Share of good weeks in one decade for one calendar week (0 to 1)."""
    day = date.fromisocalendar(2021, calendar_week, 3)
    factor = resort_factor(row["resort_id"])
    days = [day + timedelta(days=i) for i in range(-3, 4)]
    base = week_chance(snow_altitude(row), days, factor, decade_shift_m(decade))
    noise = random.Random(f"{row['resort_id']}-{decade}-{calendar_week}").uniform(-0.04, 0.04)
    return min(max(base + noise, 0.0), 1.0)


def daily_forecast(row, days: list[date]) -> pd.DataFrame:
    """Expected depth per day with an 80% band (about +-1.28 standard deviations)."""
    factor = resort_factor(row["resort_id"])
    rows = []
    for d in days:
        depth = expected_depth_cm(snow_altitude(row), d, factor)
        band = 1.28 * _spread_cm(depth)
        rows.append({"date": d, "expected_cm": depth, "low_cm": max(depth - band, 0.0), "high_cm": depth + band})
    return pd.DataFrame(rows)


def validation_table() -> pd.DataFrame:
    """Hard-coded, plausible walk-forward results (accuracy: higher is better, Brier: lower is better)."""
    rows = [
        ("Round 1", "1950-1969", "1970-1979", 0.78, 0.71, 0.165, 0.215),
        ("Round 2", "1950-1979", "1980-1989", 0.80, 0.72, 0.155, 0.208),
        ("Round 3", "1950-1989", "1990-1999", 0.81, 0.72, 0.148, 0.204),
        ("Round 4", "1950-1999", "2000-2009", 0.83, 0.73, 0.138, 0.199),
        ("Final check", "1950-2014", "2015-2025", 0.84, 0.74, 0.130, 0.194),
    ]
    return pd.DataFrame(rows, columns=[
        "round", "train_period", "test_period", "model_accuracy", "baseline_accuracy",
        "model_brier", "baseline_brier"])

# ============================================================================
# Mock versions of every data_access.py function
# ============================================================================

def _validate_holiday_range(start: date, end: date) -> str | None:
    """Mock copy of the date check (the real one is location.validate_holiday_range)."""
    if end < start:
        return "The end date is before the start date."
    if (end - start).days + 1 > config.MAX_STAY_DAYS:
        return f"Please pick at most {config.MAX_STAY_DAYS} days."
    day = start
    while day <= end:
        if day.month not in config.SEASON_MONTHS:
            return "Snow-Proof covers the ski season from December to April. Please pick dates in that period."
        day += timedelta(days=1)
    return None


def _resort_row(resort_id: str) -> pd.Series:
    """Internal helper: one row of the resorts table."""
    table = resorts_table()
    match = table[table["resort_id"] == resort_id]
    if match.empty:
        raise KeyError(f"Unknown resort: {resort_id}")
    return match.iloc[0]


def get_resorts() -> pd.DataFrame:
    """All ski resorts, one row each.

    Columns: resort_id, name, canton, lat, lon (degrees), base_altitude_m, summit_altitude_m (m),
    piste_blue_km, piste_red_km, piste_black_km, total_piste_km (km), lifts (count),
    description, station_name, station_altitude_m (m), station_distance_km (km), has_station (bool).

    FUTURE SOURCE: OpenStreetMap Overpass API (resorts, pistes, lifts), altitudes from
    swisstopo / api3.geo.admin.ch, station link from MeteoSwiss Open Data.
    """
    return resorts_table()


def get_cantons() -> list[str]:
    """Cantons that have at least one resort (for the filter), sorted.

    FUTURE SOURCE: derived from get_resorts(), so it follows the OpenStreetMap data.
    """
    return sorted(get_resorts()["canton"].unique().tolist())


def get_school_holiday_cantons() -> list[str]:
    """All 26 canton codes, for the school holiday helper.

    FUTURE SOURCE: OpenHolidays API.
    """
    return cantons()


def get_resort_details(resort_id: str) -> dict:
    """All facts about one resort as a dict (same keys as the get_resorts() columns).

    FUTURE SOURCE: OpenStreetMap Overpass API, swisstopo / api3.geo.admin.ch (altitudes).
    """
    return _resort_row(resort_id).to_dict()


def get_pistes(resort_id: str) -> pd.DataFrame:
    """Piste length by difficulty.

    Columns: difficulty ("Blue (easy)", "Red (medium)", "Black (difficult)"), km (km).

    FUTURE SOURCE: OpenStreetMap Overpass API (piece:type=downhill with piste:difficulty).
    """
    row = _resort_row(resort_id)
    return pd.DataFrame({
        "difficulty": ["Blue (easy)", "Red (medium)", "Black (difficult)"],
        "km": [row["piste_blue_km"], row["piste_red_km"], row["piste_black_km"]],
    })


def get_linked_station(resort_id: str) -> dict | None:
    """The measurement station used for the snow data, or None if there is no reliable one.

    Keys: name, altitude_m (m), distance_km (km).

    FUTURE SOURCE: MeteoSwiss Open Data (station list with snow depth measurements),
    matched to the resort by distance and altitude.
    """
    row = _resort_row(resort_id)
    if not row["has_station"]:
        return None
    return {"name": row["station_name"], "altitude_m": int(row["station_altitude_m"]),
            "distance_km": float(row["station_distance_km"])}


def get_travel_time_minutes(home_address: str, resort_id: str) -> int | None:
    """Travel time by public transport in minutes, or None if the address is unknown or empty.

    FUTURE SOURCE: swisstopo / api3.geo.admin.ch (geocoding of the address) and
    transport.opendata.ch (public transport connections).
    """
    if not home_address or not home_address.strip():
        return None
    row = _resort_row(resort_id)
    return travel_minutes(home_address, row["lat"], row["lon"])


def get_school_holidays(canton: str) -> list[tuple[date, date]]:
    """School holiday periods of a canton as (start, end) pairs, for the coming winter.

    FUTURE SOURCE: OpenHolidays API. Note that Sportferien can differ by municipality.
    """
    return school_holidays(canton)


def predict_good_week(resort_id: str, start_date: date, end_date: date) -> dict:
    """Chance of a good ski week for a stay.

    A good week means at least 50 cm of snow depth on all 7 days at the linked station.
    Returns a dict with:
      available (bool), reason (str, only if not available),
      chance (0 to 1, mean over the weeks of the stay),
      baseline (0 to 1, simple historical average for the same weeks),
      weekly (DataFrame: label, week_start, week_end, chance, baseline),
      daily (DataFrame: date, expected_cm, low_cm, high_cm; snow depth in cm).

    FUTURE SOURCE: our own trained ML model (inputs: MeteoSwiss snow history and
    Open-Meteo Historical / ERA5 weather features).
    """
    row = _resort_row(resort_id)
    if not row["has_station"]:
        return {"available": False, "reason": "No reliable measurement station nearby."}
    problem = _validate_holiday_range(start_date, end_date)
    if problem:
        return {"available": False, "reason": problem}

    factor = resort_factor(resort_id)
    altitude = snow_altitude(row)
    weeks = split_into_weeks(start_date, end_date)
    weekly_rows = []
    for days in weeks:
        calendar_week = days[0].isocalendar().week
        history = get_historical_good_week_share(resort_id, calendar_week)
        weekly_rows.append({
            "label": f"{days[0]:%d %b} to {days[-1]:%d %b}",
            "week_start": days[0], "week_end": days[-1],
            "chance": week_chance(altitude, days, factor),
            "baseline": float(history["share"].mean()),
        })
    weekly = pd.DataFrame(weekly_rows)
    all_days = [d for days in weeks for d in days]
    return {
        "available": True,
        "chance": float(weekly["chance"].mean()),
        "baseline": float(weekly["baseline"].mean()),
        "weekly": weekly,
        "daily": daily_forecast(row, all_days),
    }


def get_historical_good_week_share(resort_id: str, calendar_week: int) -> pd.DataFrame:
    """Share of good weeks for one ISO calendar week, per decade.

    Columns: decade (e.g. "1950s"), share (0 to 1).

    FUTURE SOURCE: MeteoSwiss Open Data (measured snow depth at the linked station).
    """
    row = _resort_row(resort_id)
    decades = range(1950, 2030, 10)
    return pd.DataFrame({
        "decade": [f"{d}s" for d in decades],
        "share": [historical_share(row, calendar_week, d) for d in decades],
    })


def get_validation_results() -> pd.DataFrame:
    """Walk-forward validation results of the model versus the simple historical baseline.

    Columns: round, train_period, test_period, model_accuracy, baseline_accuracy
    (share of correct yes/no calls, higher is better), model_brier, baseline_brier
    (probability error, lower is better).

    FUTURE SOURCE: our own trained ML model (output of the validation script).
    """
    return validation_table()


def get_model_info(resort_id: str) -> dict:
    """Short facts for the model info box of one resort.

    Keys: station (dict or None), training_period (str), final_test_period (str),
    final_accuracy, final_brier (floats, from the final check).

    FUTURE SOURCE: our own trained ML model (metadata and final validation scores).
    """
    final = get_validation_results().iloc[-1]
    return {
        "station": get_linked_station(resort_id),
        "training_period": final["train_period"],
        "final_test_period": final["test_period"],
        "final_accuracy": float(final["model_accuracy"]),
        "final_brier": float(final["model_brier"]),
    }


def get_ranked_resorts(resort_ids: tuple[str, ...], start_date: date, end_date: date,
                       home_address: str = "") -> pd.DataFrame:
    """Resorts ranked by chance of a good week (best first). Resorts without a station are left out.

    Columns: resort_id, name, canton, chance (0 to 1), baseline (0 to 1), travel_minutes (min or None).

    FUTURE SOURCE: predictions from our own ML model, travel time from transport.opendata.ch.
    """
    rows = []
    for rid in resort_ids:
        result = predict_good_week(rid, start_date, end_date)
        if not result["available"]:
            continue
        details = get_resort_details(rid)
        rows.append({
            "resort_id": rid, "name": details["name"], "canton": details["canton"],
            "chance": result["chance"], "baseline": result["baseline"],
            "travel_minutes": get_travel_time_minutes(home_address, rid),
        })
    columns = ["resort_id", "name", "canton", "chance", "baseline", "travel_minutes"]
    table = pd.DataFrame(rows, columns=columns)
    return table.sort_values("chance", ascending=False).reset_index(drop=True)
