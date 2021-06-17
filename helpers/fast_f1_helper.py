from datetime import datetime

import fastf1 as ff1

from classes.fastest_lap import FastestLap
from classes.free_practice_result import FreePracticeResult
from classes.session_results_group import SessionResultsGroup
from helpers.drivers_helper import get_driver_by_code


def get_fastest_laps_from_session(session_name, session_type):
    session = ff1.get_session(2021, session_name, session_type)
    session.load_laps()
    sorted_laps = session.laps.sort_values(by='LapTime')
    unique = sorted_laps.drop_duplicates(subset=['DriverNumber'])

    session_results = []
    for index, row in unique.iterrows():
        driver = get_driver_by_code(row['Driver'])
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
    print(f'SessionName: {session_name}\nSessionType: {session_type}\nDriver: {driver}')

    race = ff1.get_session(2021, session_name, session_type)
    laps = race.load_laps(with_telemetry=True)
    fastest = laps.pick_driver(driver)

    return fastest.get_telemetry()


def get_weather(session_name, session_type):
    session = ff1.get_session(2021, session_name, session_type)
    session.load_laps()
    return session.laps.get_weather_data()
