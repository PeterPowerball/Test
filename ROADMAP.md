# Roadmap

Deadline: **10.12.2026**. Tick the boxes (`[x]`) as you go, in a pull request.

## Who waits for whom

```
Nico: download (Task 3, 5) -> database (Task 4) -> coverage check -> labels (with Julian)
                                                                        |
Julian: (reads up on scikit-learn)  ............................  features -> baseline -> walk-forward -> final model -> predictions
                                                                                                                         |
Jan: swisstopo, transport, holidays, filters (Task 8) -> ranking (Task 9) ---------------------------------------------> |
                                                                                                                         v
Noah: whole UI on MOCK data (Task 10, 11), from day 1 ------------------------------------------------------> Fabio: integration
                                                                                                              (USE_MOCK_DATA = False)
```

- **The data and the 7-day labels must be done before model training starts** (Julian waits for Nico).
- **The coverage check decides the training years** (Julian and Nico decide together, then update `ml/evaluate.py`).
- **The UI is built in parallel on mock data** (Noah does not wait for anyone).
- Jan's filters work on mock data first, the real travel times come later.
- Integration (Fabio) needs the predictions from step 5.

## Milestone 0: Setup (until 26.10.2026)

- [ ] Everyone: clone, virtual environment, `streamlit run streamlit_app.py` works locally `[ALL]`
- [ ] Everyone: install Todo Tree, find your own TODOs `[ALL]`
- [ ] Deploy the skeleton on Streamlit Community Cloud `[FABIO]`
- [ ] Agree on the git workflow (README) and a weekly meeting `[FABIO]`

## Milestone 1: Data in, UI on mock data (until 08.11.2026)

- [ ] `meteoswiss.list_stations`, `fetch_snow_depth` for 3 test stations `[NICO]`
- [ ] `database.fetch_with_cache`, `get_connection`, `create_tables`, `save_table`, `load_table` `[NICO]`
- [ ] `open_meteo.fetch_weather` `[NICO]`
- [ ] `overpass`: ski areas, pistes, lifts, `compute_piste_km` `[NICO]`
- [ ] `swisstopo.search_place`, `get_altitude`; `transport.find_nearest_stop`; `holidays.fetch_school_holidays` `[JAN]`
- [ ] `filters.validate_holiday_range`, `default_trip_dates`, `filter_by_canton` `[JAN]`
- [ ] Session state, sidebar, map with clicks, legend, resort card (on mock data) `[NOAH]`
- [ ] Read up: scikit-learn LogisticRegression and RandomForest, Brier score `[JULIAN]`

## Milestone 2: Database and labels (until 15.11.2026)

- [ ] `scripts/01` and `02` run for all stations and resorts `[NICO]`
- [ ] **Coverage check** done and discussed: training years fixed in `ml/evaluate.py` `[NICO+JULIAN]`
- [ ] `clean_snow_daily`, `map_stations_to_resorts` `[NICO]`
- [ ] **Label tests written** (`tests/test_labels.py`) and `label_good_weeks` passes them `[NICO+JULIAN]`
- [ ] `scripts/03` fills `weekly_labels` `[NICO+JULIAN]`
- [ ] Snow check UI: dates, chance bar, charts, model info box (mock data) `[NOAH]`
- [ ] Travel time filter and real travel times `[JAN]`

## Milestone 3: Model (until 26.11.2026)

- [ ] `features.build_features`, `add_past_good_week_share` (check the leakage warning!) `[JULIAN]`
- [ ] `baseline.compute_baseline` `[JULIAN]`
- [ ] `evaluate`: split, metrics, walk-forward rounds `[JULIAN]`
- [ ] `train`: two or more candidate models, choose the best `[JULIAN+JAN]`
- [ ] Final check run ONCE, results saved in `model_runs` `[JULIAN]`
- [ ] `ranking.rank_resorts`, ranked list in the UI `[JAN+NOAH]`
- [ ] "About our model" page with timeline and comparison charts `[NOAH+JULIAN]`

## Milestone 4: Integration (until 03.12.2026)

- [ ] `scripts/05` fills `weekly_predictions`; `predict.predict_good_week` `[JULIAN+JAN]`
- [ ] Real versions of all `data_access.py` functions `[FABIO, JAN, JULIAN]`
- [ ] Switch `config.USE_MOCK_DATA = False`, fix everything that breaks `[FABIO]`
- [ ] Set `SKELETON_PREVIEW = False` in `pages/explore.py` `[NOAH]`
- [ ] Delete `mock_access.py` and `mock_data.py` when nothing uses them anymore `[FABIO]`
- [ ] All tests pass, app deployed `[FABIO]`

## Milestone 5: Video and documentation (until 09.12.2026)

- [ ] 4-minute demo video, own voice-over (not AI-generated), everyone shows their part `[ALL]`
- [ ] `CONTRIBUTIONS.md` complete `[ALL]`
- [ ] `GENAI_LOG.md` complete, GenAI reflection for the video `[ALL]`
- [ ] Final review against the grading map in README.md `[FABIO]`

## Deadline: 10.12.2026

- [ ] Submit `[FABIO]`

## Optional (only if everything above is done)

- [ ] SLF as a second snow source (`data_sources/slf.py`) `[NICO]`
- [ ] Decade trend chart, similar resorts `[JULIAN, JAN, NOAH]`
- [ ] Future outlook page (Use Case 2), set `config.SHOW_FUTURE_PAGE = True` `[ALL]`
