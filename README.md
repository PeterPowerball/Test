# Snow-Proof

Snow-Proof is a Streamlit web app that shows all Swiss ski resorts on a map. Click a resort to see its slopes
and key facts, then check the chance of good snow for your holiday dates. A **good ski week** means at least
50 cm of snow depth on all 7 days at the linked measurement station. Later, the chance will come from our own
machine learning model trained on decades of MeteoSwiss snow data and Open-Meteo weather data.

**Status: UI prototype. Every number is mock data.** There are no API calls and no API keys.

Group project at the University of St. Gallen (HSG), course "Fundamentals and Methods of Computer Science for Business Studies".

![Screenshot placeholder](docs/screenshot.png)

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Run the tests with `pip install pytest` and then `pytest`.

## Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **Create app** and choose to deploy from a GitHub repository.
3. Select this repository and the branch you want to deploy.
4. Set the main file path to `streamlit_app.py`.
5. Click **Deploy**. The first start takes a few minutes while the requirements are installed.

Private repositories work too, once you have authorized Streamlit to access them in your GitHub settings.

## Project structure

```
streamlit_app.py        entry point: page config and navigation
pages/                  explore.py (main page), model.py, future.py
snowproof/
    data_access.py      the ONLY place the UI gets data from
    mock_data.py        mock resorts, stations, predictions (to be replaced)
    ui_components.py    reusable pieces: map, gauge, charts
    config.py           colors and constants (50 cm threshold, season months)
tests/test_app_smoke.py smoke tests with streamlit.testing.v1.AppTest
```

## Where to plug in real data

The pages never touch `mock_data.py`. Replace one function in `snowproof/data_access.py` at a time and keep
the returned columns the same. Each docstring describes the exact format.

| Function | Future real source | Team area |
|---|---|---|
| `get_resorts`, `get_resort_details`, `get_pistes` | OpenStreetMap Overpass API (resorts, pistes, lifts), swisstopo / api3.geo.admin.ch (altitudes) | Data and database (Nico) |
| `get_linked_station` | MeteoSwiss Open Data | Data and database (Nico) |
| `get_historical_good_week_share` | MeteoSwiss Open Data (measured snow depth) | Data and database (Nico) |
| `predict_good_week`, `get_model_info`, `get_future_outlook` | Our own trained ML model (plus Open-Meteo Historical / ERA5 features) | ML model (Julian, Jan) |
| `get_validation_results` | Our own ML model (validation script output) | ML model (Julian, Jan) |
| `get_travel_time_minutes` | swisstopo geocoding and transport.opendata.ch | Filters and ranking (Jan) |
| `get_school_holidays`, `get_school_holiday_cantons` | OpenHolidays API | Filters and ranking (Jan) |
| `get_ranked_resorts`, `get_alternatives`, `get_cantons` | Built on the functions above | Filters and ranking (Jan) |
| Pages and `ui_components.py` | n/a | UI, map and charts (Noah) |
| `streamlit_app.py`, tests, deployment | n/a | Integration (Fabio) |

## Known limitations

- All numbers are mock data and deterministic (seeded by resort id).
- Travel times are only mocked for a few Swiss cities (Zurich, Bern, Basel, Geneva, Lausanne, St. Gallen, Lucerne, Lugano, Chur, Winterthur, Sion).
- School holiday dates are placeholders.
- The map needs internet access for the swisstopo tiles. A CartoDB layer can be switched on in the layer control.
