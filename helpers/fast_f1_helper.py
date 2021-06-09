from datetime import datetime

import fastf1 as ff1

from classes.fastest_lap import FastestLap
from classes.free_practice_result import FreePracticeResult
from classes.session_results_group import SessionResultsGroup
from helpers import functions


def get_weekend_results(weekend_name):
    weekend = ff1.get_session(2021, weekend_name)

    fp1_results = get_fastest_laps_from_session(weekend.get_practice(1))
    fp2_results = get_fastest_laps_from_session(weekend.get_practice(2))
    fp3_results = get_fastest_laps_from_session(weekend.get_practice(3))
    quali = get_fastest_laps_from_session(weekend.get_quali())
    race = get_fastest_laps_from_session(weekend.get_race())


def get_fastest_laps_from_session(session_name, session_type):
    session = ff1.get_session(2021, session_name, session_type)
    session.load_laps()
    sorted_laps = session.laps.sort_values(by='LapTime')
    unique = sorted_laps.drop_duplicates(subset=['DriverNumber'])

    session_results = []
    for index, row in unique.iterrows():
        driver = functions.get_driver_by_code(row['Driver'])
        fastest_lap = FastestLap(index + 1, row['LapNumber'], str(row['LapTime']), '')
        fp_res = FreePracticeResult(index + 1, driver, fastest_lap)

        session_results.append(fp_res)

    session_result_group = SessionResultsGroup(datetime.now(), session_results)

    return session_result_group


def get_laps(session_name, session_type):
    session = ff1.get_session(2021, session_name, session_type)
    session.load_laps()
    return session.laps


def get_telemetry(session_name, session_type, driver):
    session = ff1.get_session(2021, session_name, session_type)
    session.load_laps(with_telemetry=True)
    return session.laps.pick_driver(driver).get_telemetry()
