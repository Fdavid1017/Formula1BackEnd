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


def get_car_data(session_name, session_type, driver, from_lap=-1, till_lap=-1):
    print(f'SessionName: {session_name}\nSessionType: {session_type}\nDriver: {driver}')

    print('1')
    race = ff1.get_session(2021, session_name, session_type)
    laps = race.load_laps(with_telemetry=True)
    driver_laps = laps.pick_driver(driver)

    print('2')
    if from_lap < 0 or till_lap < 0:
        from_lap = 0
        till_lap = len(driver_laps.index)

    if till_lap > len(driver_laps.index):
        till_lap = len(driver_laps.index)

    print('3')
    telemetry = []
    telemetry_index = 0
    for i in range(from_lap, till_lap):
        l = driver_laps.iloc[i]
        print('4')
        tel = l.get_car_data()
        print('5')
        tel = tel.add_distance()
        # print('6')
        # tel = tel.add_driver_ahead()
        print('7')
        telemetry.append(tel)
        print('8')
        telemetry[telemetry_index]['Compound'] = l['Compound']
        print('9')
        telemetry[telemetry_index]['TyreLife'] = l['TyreLife']
        print('10')
        telemetry[telemetry_index]['TrackStatus'] = l['TrackStatus']
        print('11')
        telemetry_index = telemetry_index + 1
        print('12')

    return telemetry


def get_car_position(session_name, session_type, driver, from_lap=-1, till_lap=-1):
    print(f'SessionName: {session_name}\nSessionType: {session_type}\nDriver: {driver}')

    race = ff1.get_session(2021, session_name, session_type)
    laps = race.load_laps(with_telemetry=True)
    driver_laps = laps.pick_driver(driver)

    if from_lap < 0 or till_lap < 0:
        from_lap = 0
        till_lap = len(driver_laps.index)

    if till_lap > len(driver_laps.index):
        till_lap = len(driver_laps.index)

    positions = []
    for i in range(from_lap, till_lap):
        l = driver_laps.iloc[i]
        pos = l.get_pos_data()
        positions.append(pos)

    return positions


def get_weather(session_name, session_type):
    session = ff1.get_session(2021, session_name, session_type)
    session.load_laps()
    return session.laps.get_weather_data()
