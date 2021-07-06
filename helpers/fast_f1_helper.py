from datetime import datetime

import fastf1 as ff1

from classes.fastest_lap import FastestLap
from classes.free_practice_result import FreePracticeResult
from classes.session_results_group import SessionResultsGroup
from helpers.drivers_helper import get_all_driver


def get_fastest_laps_from_session(session_name, session_type):
    session = ff1.get_session(2021, session_name, session_type)
    laps = session.load_laps()
    drivers = get_all_driver()

    fastest_laps = []

    for i in range(len(drivers)):
        driver = drivers[i]
        try:
            fl = laps.pick_driver(driver.code).pick_fastest()
            fastest_lap = FastestLap(int(fl['LapNumber']), str(fl['LapTime']), '')
            fp_res = FreePracticeResult(int(i + 1), driver, fastest_lap)

            fastest_laps.append(fp_res)
        except:
            print(driver.code + ' error getting laps (possibly no lap data)')

    fastest_laps.sort(key=lambda x: x.fastest_lap.time)
    for index in range(len(fastest_laps)):
        fastest_laps[index].position = index + 1

    return SessionResultsGroup(datetime.now(), fastest_laps)


def get_laps(session_name, session_type):
    session = ff1.get_session(2021, session_name, session_type)
    session.load_laps()
    return session.laps


def get_telemetry(session_name, session_type, driver):
    print(f'SessionName: {session_name}\nSessionType: {session_type}\nDriver: {driver}')

    race = ff1.get_session(2021, session_name, session_type)
    laps = race.load_laps(with_telemetry=True)
    driver_laps = laps.pick_driver(driver)

    return driver_laps.get_telemetry()


def get_car_data(session_name, session_type, driver):
    print(f'SessionName: {session_name}\nSessionType: {session_type}\nDriver: {driver}')

    race = ff1.get_session(2021, session_name, session_type)
    laps = race.load_laps(with_telemetry=True)
    driver_laps = laps.pick_driver(driver)

    telemetry = []
    for i in range(len(driver_laps.index)):
        l = driver_laps.iloc[i]
        tel = l.get_car_data()
        telemetry.append(tel)

    return telemetry


def get_car_position(session_name, session_type, driver):
    print(f'SessionName: {session_name}\nSessionType: {session_type}\nDriver: {driver}')

    race = ff1.get_session(2021, session_name, session_type)
    laps = race.load_laps(with_telemetry=True)
    driver_laps = laps.pick_driver(driver)

    positions = []
    for i in range(len(driver_laps.index)):
        l = driver_laps.iloc[i]
        pos = l.get_pos_data()
        positions.append(pos)

    return positions


def get_weather(session_name, session_type):
    session = ff1.get_session(2021, session_name, session_type)
    session.load_laps()
    return session.laps.get_weather_data()
