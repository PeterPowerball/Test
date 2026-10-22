"""
pipeline.py: download the data, build the database, create labels, train the model, save predictions.

Owner:       Nico (steps 1 to 3), Julian (steps 4 and 5), Jan (his parts of steps 1 and 5)
Depends on:  snowproof/data.py, snowproof/location.py, snowproof/model.py
Used by:     run by hand from the repository root, never by the app:
                 python pipeline.py        runs all steps in order
                 python pipeline.py 3      runs only step 3
Flow:        Steps 1 to 5. Afterwards Fabio sets config.USE_MOCK_DATA = False and the app shows real data.

Why separate from the app? Downloading 50+ years of data and training take minutes. The website
must never do this on a click. It only reads the results from the database.
"""

import sys

from snowproof import config, data, location, model


def step1_download_data() -> None:
    """
    STEP 1 OF 5: download stations, snow depth, weather, resorts, pistes, lifts, stops and holidays.

    Owner:    Nico (Task 3 and 5), Jan (Task 8)
    Returns:  nothing (everything ends up in config.RAW_DIR and the database)
    """
    # TODO [NICO | Task 3] Download step by step
    # Step 1: stations = data.list_stations(). Print how many you got.
    # Step 2: For each station: data.fetch_with_cache(f"snow_{code}", data.fetch_snow_depth,
    #         code, date(1930, 1, 1), date.today()). Then data.save_snow_daily(...).
    # Step 3: Same idea for data.fetch_weather (from 1950, ERA5 starts there).
    # Step 4: Resorts, pistes and lifts from OpenStreetMap (cached), then data.compute_piste_km.
    # Hint:   Start with 3 stations (DAV, WFJ and one low station) until everything works. Then run all.
    # Hint:   Print progress ("12 of 85 stations done"), downloads take a while.
    # Done when: config.RAW_DIR contains files and a second run finishes in seconds.
    # TODO [JAN | Task 8] Add holidays and transport stops here
    # Step 1: location.fetch_school_holidays for the coming winter -> data.save_table(..., "holiday_periods").
    # Step 2: For each resort: location.find_nearest_stop(lat, lon) -> data.save_table(..., "transport_stops").
    # Done when: both tables have rows.
    raise NotImplementedError("TODO [NICO | Task 3]: step1_download_data")


def step2_build_database() -> None:
    """
    STEP 2 OF 5: create all tables, save the downloaded data, and link stations to resorts.

    Owner:    Nico (Task 4: database and data preparation)
    Returns:  nothing
    """
    # TODO [NICO | Task 4] Build the database
    # Step 1: data.create_tables().
    # Step 2: Save stations, resorts, pistes (with resort_id), weather into their tables (data.save_table).
    # Step 3: Per resort: piste km per difficulty, number of lifts, base and summit altitude
    #         (location.get_altitude for the lowest and highest piste point). Update the resorts table.
    # Step 4: mapping = data.map_stations_to_resorts(resorts, stations) -> "resort_station_mapping".
    # Step 5: Print a short summary: number of rows per table.
    # Done when: the summary shows rows in stations, resorts, snow_daily, pistes and resort_station_mapping.
    raise NotImplementedError("TODO [NICO | Task 4]: step2_build_database")


def step3_prepare_labels() -> None:
    """
    STEP 3 OF 5: coverage check, cleaning, and the weekly labels (good week: 1, 0 or unknown).
    The labels are the hand-over point from data (Nico) to model (Julian). Do this together.

    Owner:    Nico + Julian (Task 4 and Task 6)
    Returns:  nothing
    """
    # TODO [NICO+JULIAN | Task 4] Prepare the labels
    # Step 1: snow = data.load_table("snow_daily").
    # Step 2: coverage = data.check_station_coverage(snow). Print it and save it as a CSV for the team.
    #         DISCUSS with Julian: which years can we train on? Update model.WALK_FORWARD_ROUNDS if needed.
    # Step 3: clean = data.clean_snow_daily(snow).
    # Step 4: labels = data.label_good_weeks(clean) -> data.save_table(labels, "weekly_labels").
    # Step 5: Print the share of 1, 0 and unknown labels.
    # Done when: tests/test_labels.py passes and weekly_labels has rows for every station.
    raise NotImplementedError("TODO [NICO+JULIAN | Task 4]: step3_prepare_labels")


def step4_train_and_validate() -> None:
    """
    STEP 4 OF 5: compare the candidate models with walk-forward validation, run the final check once,
    save the best model.

    Owner:    Julian (Task 6 and 7), Jan (support)
    Returns:  nothing
    """
    # TODO [JULIAN | Task 7] Train and validate
    # Step 1: Load weekly_labels and stations, build the feature table (model.build_features).
    # Step 2: For each name in model.CANDIDATE_MODELS: model.run_walk_forward(...) WITHOUT the final check.
    # Step 3: best = model.choose_best_model(results). Print all results so you can compare.
    # Step 4: Only now, ONCE: run the final check for the best model (include_final_check=True).
    # Step 5: Save the rounds to the model_runs table (data.save_table) for the "About our model" page.
    # Step 6: Train the best model on ALL years and save it (model.save_model).
    # Hint:   If you go back and change the model after seeing the final check, the final check
    #         is no longer honest. Write down what you did (GENAI_LOG.md / the video).
    # Done when: models/good_week_model.joblib exists and model_runs has 5 rows for the final model.
    raise NotImplementedError("TODO [JULIAN | Task 7]: step4_train_and_validate")


def step5_save_predictions() -> None:
    """
    STEP 5 OF 5: for every station and every possible week start of the coming season,
    precompute chance and baseline for the app.

    Owner:    Julian + Jan (Task 7 and Task 9)
    Returns:  nothing (fills the weekly_predictions table)
    """
    # TODO [JULIAN+JAN | Task 7] Precompute predictions
    # Step 1: trained = model.load_model(). Load stations that have a reliable resort mapping.
    # Step 2: For each station and each day from 1 December to 24 April of the coming season
    #         (each day is a possible week start): chance = model.predict_chance(...).
    # Step 3: baseline: model.compute_baseline(labels, (first year, last year)) for the same calendar week.
    # Step 4: Save everything to weekly_predictions (station_code, week_start, calendar_week, chance, baseline).
    # Done when: weekly_predictions has about 145 rows per station, and the app shows them
    #            after setting config.USE_MOCK_DATA = False.
    raise NotImplementedError("TODO [JULIAN+JAN | Task 7]: step5_save_predictions")


STEPS = [step1_download_data, step2_build_database, step3_prepare_labels,
         step4_train_and_validate, step5_save_predictions]

if __name__ == "__main__":
    # "python pipeline.py" runs all steps, "python pipeline.py 3" only step 3
    chosen = [int(arg) for arg in sys.argv[1:]] or [1, 2, 3, 4, 5]
    for number in chosen:
        print(f"--- Step {number}: {STEPS[number - 1].__name__}")
        STEPS[number - 1]()
