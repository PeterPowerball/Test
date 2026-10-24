# Snow-Proof

Snow-Proof is a Streamlit web app that shows all Swiss ski resorts on a map. Click a resort to see its slopes and key
facts, then check the chance of a **good ski week** for your holiday dates: at least 50 cm of measured snow depth on all
7 days at the linked MeteoSwiss station. The chance comes from **our own machine learning model**, trained on decades of
measured snow depth (MeteoSwiss) and historical weather (Open-Meteo), and it is always compared with the simple
historical average.

**Status: code skeleton.** Every function exists with its inputs, outputs and a TODO. The app already runs: sections that
are not built yet show a 🚧 box, and the UI uses mock data until the real pipeline works. The finished look is on the
`ui-prototype` branch.

## Project structure: one main file per person

```
streamlit_app.py          starts the app, navigation                         [FABIO]
pipeline.py               steps 1 to 5: download, database, labels,          [NICO, JULIAN, JAN]
                          train, predictions (run by hand, never by the app)
pages/
    explore.py            map, filters, resort card, snow check              [NOAH, JAN]
    about_model.py        "About our model" page                             [NOAH, JULIAN]
    about_us.py           "About us" page                                    [NOAH]
snowproof/
    config.py             all settings, URLs, USE_MOCK_DATA switch           [FABIO]
    data.py               download, database, cleaning, 7-day labels         [NICO] (+ JULIAN for labels)
    model.py              features, baseline, training, validation, predict  [JULIAN] (+ JAN)
    location.py           places, travel time, holidays, filters, ranking    [JAN]
    ui.py                 map, resort card, chance bar, charts, todo_box     [NOAH]
    data_access.py        the ONLY place the app gets data from              [FABIO + owners]
    mock_data.py          fake data from the prototype (delete at the end)
tests/
    test_app_smoke.py     app starts, all pages load                         [FABIO]
    test_labels.py        test cases for the 7-day rule                      [NICO+JULIAN]
data/, models/            created by pipeline.py (not on GitHub)
CONTRIBUTIONS.md          who did what                                       [ALL]
GENAI_LOG.md              our AI use log                                     [ALL]
```

Each file starts with a short list of its sections, in the order you build them.

**Mock data switch:** while `config.USE_MOCK_DATA = True`, every function in `data_access.py` returns fake data from
`mock_data.py`. Noah can build the whole UI now. Fabio switches it to `False` when `pipeline.py` has run.

## Setup

```bash
git clone https://github.com/PeterPowerball/Test.git
cd Test
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

- Tests: `pip install pytest`, then `pytest`. A 🚧 box is fine, a red error is not.
- Data and model: `python pipeline.py` runs all 5 steps, `python pipeline.py 3` runs only step 3.



## Find your tasks

Every place where someone has to code has a TODO block like this:

```python
# TODO [NICO | Task 3] Download measured snow depth from MeteoSwiss
# Step 1: ...
# Done when: ...
raise NotImplementedError("TODO [NICO | Task 3]: fetch_snow_depth")
```

- In VS Code, search the whole project (Ctrl+Shift+F / Cmd+Shift+F) for `TODO [YOURNAME` (for example `TODO [NICO`).
  Shared tasks look like `TODO [NICO+JULIAN`, so this search finds them too.
- Install the VS Code extension **Todo Tree** to see all TODOs in a side panel, grouped by file.
- The **Roadmap** below says in which order to work and who waits for whom.
- Remove the `raise NotImplementedError(...)` line only when your function really works.

| Tag | Person | Tasks | Main file |
|---|---|---|---|
| `[FABIO]` | Fabio | 1 Project management, 2 Technical foundation, 12 Integration and testing, 13 Final review | `data_access.py`, `config.py`, `streamlit_app.py` |
| `[NICO]` | Nico | 3 Snow and weather data, 4 Database and data preparation, 5 Ski resort information | `data.py` |
| `[JULIAN]` | Julian | 6 Model training, 7 Model evaluation and prediction function | `model.py` |
| `[JAN]` | Jan | 8 Location, travel and holiday filters, 9 Resort ranking | `location.py` |
| `[NOAH]` | Noah | 10 User interface and navigation, 11 Map, charts and resort details | `ui.py`, `pages/` |
| `[ALL]` | Everyone | Video, contribution documentation, GenAI reflection | `CONTRIBUTIONS.md`, `GENAI_LOG.md` |

## Git workflow for beginners

1. Always start from the newest `main`: `git checkout main` and `git pull`.
2. Make **one branch per person and topic**, e.g. `git checkout -b nico/meteoswiss` or `noah/map`.
3. Make **small commits** with clear messages: `git add <files>` and `git commit -m "Download snow depth for one station"`.
4. Push your branch (`git push -u origin nico/meteoswiss`) and open a **pull request into `main`** on GitHub.
   Ask one teammate to look at it before merging.
5. **Work in your own file. Don't change someone else's file without talking to them first.**
6. Run `pytest` before every pull request.

## Roadmap

Deadline: **10.12.2026**. Tick the boxes (`[x]`) as you go, in a pull request.

**Who waits for whom**

- **The data and the 7-day labels must be done before model training starts** (Julian waits for Nico).
- **The coverage check decides the training years** (Nico and Julian decide together, then update
  `WALK_FORWARD_ROUNDS` in `model.py`).
- **The UI is built in parallel on mock data** (Noah does not wait for anyone).
- Jan's filters work on mock data first, the real travel times come later.
- Integration (Fabio) needs the predictions from `pipeline.py` step 5.

### Milestone 0: Setup (until 26.10.2026)

- [ ] Everyone: clone, virtual environment, `streamlit run streamlit_app.py` works locally `[ALL]`
- [ ] Everyone: install Todo Tree, find your own TODOs `[ALL]`
- [ ] Deploy the skeleton on Streamlit Community Cloud `[FABIO]`
- [ ] Agree on the git workflow and a weekly meeting `[FABIO]`

### Milestone 1: Data in, UI on mock data (until 08.11.2026)

- [ ] `data.py`: `list_stations`, `fetch_snow_depth` for 3 test stations `[NICO]`
- [ ] `data.py`: `fetch_with_cache`, `get_connection`, `create_tables`, `save_table`, `load_table` `[NICO]`
- [ ] `data.py`: `fetch_weather`; ski areas, pistes, lifts, `compute_piste_km` `[NICO]`
- [ ] `location.py`: `search_place`, `get_altitude`, `find_nearest_stop`, `fetch_school_holidays` `[JAN]`
- [ ] `location.py`: `validate_holiday_range`, `default_trip_dates`, `filter_by_canton` `[JAN]`
- [ ] `ui.py` and `pages/explore.py`: session state, sidebar, map with clicks, legend, resort card (mock data) `[NOAH]`
- [ ] Read up: scikit-learn LogisticRegression and RandomForest, Brier score `[JULIAN]`

### Milestone 2: Database and labels (until 15.11.2026)

- [ ] `pipeline.py` steps 1 and 2 run for all stations and resorts `[NICO]`
- [ ] **Coverage check** done and discussed, training years fixed in `model.py` `[NICO+JULIAN]`
- [ ] `clean_snow_daily`, `map_stations_to_resorts` `[NICO]`
- [ ] **Label tests written** (`tests/test_labels.py`) and `label_good_weeks` passes them `[NICO+JULIAN]`
- [ ] `pipeline.py` step 3 fills `weekly_labels` `[NICO+JULIAN]`
- [ ] Snow check UI: dates, chance bar, charts, model info box (mock data) `[NOAH]`
- [ ] Travel time filter and real travel times `[JAN]`

### Milestone 3: Model (until 26.11.2026)

- [ ] `build_features`, `add_past_good_week_share` (read the leakage warning!) `[JULIAN]`
- [ ] `compute_baseline` `[JULIAN]`
- [ ] Walk-forward: `split_by_years`, `compute_metrics`, `run_walk_forward` `[JULIAN]`
- [ ] Two or more candidate models, `choose_best_model` `[JULIAN+JAN]`
- [ ] Final check run ONCE (`pipeline.py` step 4), results saved in `model_runs` `[JULIAN]`
- [ ] `rank_resorts`, ranked list in the UI `[JAN+NOAH]`
- [ ] "About our model" page with timeline and comparison charts `[NOAH+JULIAN]`

### Milestone 4: Integration (until 03.12.2026)

- [ ] `pipeline.py` step 5 fills `weekly_predictions`; `model.predict_good_week` `[JULIAN+JAN]`
- [ ] Real versions of all `data_access.py` functions `[FABIO, JAN, JULIAN]`
- [ ] Switch `config.USE_MOCK_DATA = False`, fix everything that breaks `[FABIO]`
- [ ] Set `SKELETON_PREVIEW = False` in `pages/explore.py` `[NOAH]`
- [ ] Delete `mock_data.py` when nothing uses it anymore `[FABIO]`
- [ ] All tests pass, app deployed `[FABIO]`

### Milestone 5: Video and documentation (until 09.12.2026)

- [ ] 4-minute demo video, own voice-over (not AI-generated), everyone shows their part `[ALL]`
- [ ] `CONTRIBUTIONS.md` complete `[ALL]`
- [ ] `GENAI_LOG.md` complete, GenAI reflection for the video `[ALL]`
- [ ] Final review against the grading map below `[FABIO]`

### Deadline: 10.12.2026

- [ ] Submit `[FABIO]`

### Optional (only if everything above is done)

- [ ] SLF as a second snow source (`fetch_slf_snow_depth` in `data.py`) `[NICO]`
- [ ] Decade trend chart, similar resorts with better chances `[JULIAN, JAN, NOAH]`
- [ ] Future outlook (Use Case 2): good ski weeks per decade until 2050 from climate models, as a new page `[ALL]`.
      Seasonal forecasts (ECMWF) are not planned: our tutor advised against them.

## Grading map

| # | Course requirement | Where we cover it |
|---|---|---|
| 1 | Problem clearly stated | README (top), `pages/about_us.py`, `pages/about_model.py` section 1, the video |
| 2 | Data via API and/or database | `snowproof/data.py` and `snowproof/location.py` (6 APIs, SQLite), `pipeline.py` steps 1 and 2 |
| 3 | Data visualization | `snowproof/ui.py`: map, chance bar, snow depth chart, validation charts |
| 4 | User interaction | `pages/explore.py`: filters, map clicks, resort card, snow check with date input |
| 5 | Own trained ML model | `snowproof/model.py` and `pipeline.py` steps 4 and 5; results on the "About our model" page |
| 6 | Code documented with comments | file headers, docstrings and TODO steps in every file |
| 7 | Team contributions and GenAI use documented, shown in the video | `CONTRIBUTIONS.md`, `GENAI_LOG.md`, the video |
| 8 | 4-minute demo video with our own (not AI-generated) voice-over | recorded by everyone, see Milestone 5 |

## Data sources and attribution

MeteoSwiss Open Data, Open-Meteo (ERA5), © OpenStreetMap contributors (Overpass), © swisstopo, transport.opendata.ch,
OpenHolidays API.
