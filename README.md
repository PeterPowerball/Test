# Snow-Proof

Snow-Proof is a Streamlit web app that shows all Swiss ski resorts on a map. Click a resort to see its slopes and key
facts, then check the chance of a **good ski week** for your holiday dates: at least 50 cm of measured snow depth on all
7 days at the linked MeteoSwiss station. The chance comes from **our own machine learning model**, trained on decades of
measured snow depth (MeteoSwiss) and historical weather (Open-Meteo), and it is always compared with the simple
historical average.

Group project at the University of St. Gallen (HSG), course "Fundamentals and Methods of Computer Science for Business
Studies".

**Status: code skeleton.** Every function exists with its inputs, outputs and a TODO. The app already runs: sections that
are not built yet show a 🚧 box, and the UI uses mock data until the real pipeline works. The finished look is on the
`ui-prototype` branch.

## Setup

```bash
git clone https://github.com/PeterPowerball/Test.git
cd Test
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Tests: `pip install pytest`, then `pytest`. A 🚧 box is fine, a red error is not.

## Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **Create app**, choose this repository, the branch (`main`) and `streamlit_app.py` as the main file.
3. Click **Deploy**. Every push to that branch redeploys the app.

Private repositories work too, once Streamlit is authorized for them in your GitHub settings.

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
- **ROADMAP.md** says in which order to work and who waits for whom.
- Remove the `raise NotImplementedError(...)` line only when your function really works.

| Tag | Person | Tasks |
|---|---|---|
| `[FABIO]` | Fabio | 1 Project management, 2 Technical foundation, 12 Integration and testing, 13 Final review |
| `[NICO]` | Nico | 3 Snow and weather data, 4 Database and data preparation, 5 Ski resort information |
| `[JULIAN]` | Julian | 6 Model training, 7 Model evaluation and prediction function |
| `[JAN]` | Jan | 8 Location, travel and holiday filters, 9 Resort ranking |
| `[NOAH]` | Noah | 10 User interface and navigation, 11 Map, charts and resort details |
| `[ALL]` | Everyone | Video, contribution documentation, GenAI reflection |

## Git workflow for beginners

1. Always start from the newest `main`: `git checkout main` and `git pull`.
2. Make **one branch per person and topic**, e.g. `git checkout -b nico/meteoswiss` or `noah/map`.
3. Make **small commits** with clear messages: `git add <files>` and `git commit -m "Download snow depth for one station"`.
4. Push your branch (`git push -u origin nico/meteoswiss`) and open a **pull request into `main`** on GitHub.
   Ask one teammate to look at it before merging.
5. **Don't change someone else's file without talking to them first.** If you need a change in another file, tell the owner.
6. Run `pytest` before every pull request.

## Project structure (in chronological order)

```
streamlit_app.py                 entry point and navigation                          [FABIO]
scripts/                         run these in order, once (step 1 to 5)
    01_download_data.py          call all fetch functions                            [NICO, JAN]
    02_build_database.py         create SQLite tables, save data                     [NICO]
    03_prepare_labels.py         coverage check, cleaning, weekly labels             [NICO+JULIAN]
    04_train_and_validate.py     walk-forward validation, choose and save the model  [JULIAN]
    05_save_predictions.py       precompute chances for the app                      [JULIAN+JAN]
snowproof/
    config.py                    constants, URLs, paths, USE_MOCK_DATA               [FABIO]
    data_sources/                meteoswiss, open_meteo, overpass, slf (optional)    [NICO]
                                 swisstopo, transport, holidays                      [JAN]
    database.py                  SQLite: tables, save, load, cache                   [NICO]
    preparation.py               coverage, cleaning, station mapping, labels         [NICO(+JULIAN)]
    ml/                          features, baseline, train, evaluate, predict        [JULIAN(+JAN)]
    filters.py, ranking.py       sidebar filters and ranking                         [JAN]
    data_access.py               the ONLY data entry point for the UI                [FABIO + owners]
    mock_access.py, mock_data.py mock data from the prototype (delete at the end)
    ui_components.py             map, resort card, chance bar, charts, todo_box      [NOAH]
pages/                           explore.py, model.py (About our model), about.py, future.py (optional)
data/, models/                   created by the scripts (gitignored)
tests/                           test_app_smoke.py [FABIO], test_labels.py [NICO+JULIAN]
```

**Mock data switch:** while `config.USE_MOCK_DATA = True`, every function in `data_access.py` returns the prototype's
mock data. Noah can build the whole UI now. Fabio switches it to `False` when steps 1 to 5 are done.

## Grading map

| # | Course requirement | Where we cover it |
|---|---|---|
| 1 | Problem clearly stated | README (top), `pages/about.py`, `pages/model.py` section 1, the video |
| 2 | Data via API and/or database | `snowproof/data_sources/*.py` (6 APIs), `snowproof/database.py` (SQLite), `scripts/01` and `02` |
| 3 | Data visualization | `snowproof/ui_components.py`: map, chance bar, snow depth chart, validation charts |
| 4 | User interaction | `pages/explore.py`: filters, map clicks, resort card, snow check with date input |
| 5 | Own trained ML model | `snowproof/ml/` and `scripts/04`, `05`; results on the "About our model" page |
| 6 | Code documented with comments | file headers, docstrings and TODO steps in every file |
| 7 | Team contributions and GenAI use documented, shown in the video | `CONTRIBUTIONS.md`, `GENAI_LOG.md`, the video |
| 8 | 4-minute demo video with our own (not AI-generated) voice-over | recorded by everyone, see ROADMAP.md milestone 5 |

## Data sources and attribution

MeteoSwiss Open Data, Open-Meteo (ERA5), © OpenStreetMap contributors (Overpass), © swisstopo, transport.opendata.ch,
OpenHolidays API.
