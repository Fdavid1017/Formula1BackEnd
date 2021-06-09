from datetime import datetime

import requests
from flask import jsonify

from classes.circuit import Circuit
from classes.color_scheme import ColorScheme
from classes.constructor import Constructor
from classes.driver import Driver
from classes.fastest_lap import FastestLap
from classes.qualifying_result import QualifyingResult
from classes.race import Race
from classes.session_result import SessionResult
from classes.session_results_group import SessionResultsGroup
from helpers.circuit.circuit_helper import load_json, get_circuit


def get_schedule():
    response = requests.get('http://ergast.com/api/f1/current.json')

    if response.status_code != 200:
        return jsonify({
            'error': f'api response code {response.status_code}'
        })

    result = response.json()['MRData']['RaceTable']['Races']

    races = []
    for i in range(len(result)):
        r = result[i]

        # Race properties
        race_round = r['round']
        race_name = r['raceName']
        dt = r['date'] + ' ' + str(r['time']).replace('Z', '')
        date_time = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')

        # Circuit properties

        circuit_json = load_json('helpers/circuit/circuits.json')

        c = r['Circuit']

        current_c = get_circuit(circuit_json, c['circuitId'])

        circuit_id = c['circuitId']
        circuit_name = c['circuitName']
        city = c['Location']['locality']
        country = c['Location']['country']
        image_location = current_c['image_location']
        first_gp = current_c['first_gp']
        number_of_laps = current_c['number_of_laps']
        length = current_c['length']
        race_distance = current_c['race_distance']
        gjson_map = current_c['gjson_map']
        color_scheme = ColorScheme(current_c['primary_color'], current_c['secondary'], current_c['tertiary'])

        circuit = Circuit(circuit_id, circuit_name, city, country, image_location, first_gp, number_of_laps, length,
                          race_distance, gjson_map, color_scheme)

        race = Race(race_round, race_name, circuit, date_time)
        races.append(race.serialize())

    return jsonify(races)


def get_driver_from_ergast_data(data, constructor):
    driver_id = data['driverId']
    driver_number = data['permanentNumber']
    code = data['code']
    given_name = data['givenName']
    family_name = data['familyName']

    return Driver(driver_id, driver_number, code, given_name, family_name, constructor)


def get_constructor_from_ergast_data(data):
    constructor_id = data['constructorId']
    name = data['name']

    return Constructor(constructor_id, name)


def get_qualifying_results(gp_round):
    response = requests.get(f'http://ergast.com/api/f1/current/{gp_round}/qualifying.json')

    if response.status_code != 200:
        return jsonify({
            'error': f'api response code {response.status_code}'
        })

    result = response.json()['MRData']['RaceTable']['Races'][0]
    dt = result['date'] + ' ' + str(result['time']).replace('Z', '')
    date_time = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')

    qualifying = result['QualifyingResults']

    quali_results = []
    for i in range(len(qualifying)):
        r = qualifying[i]

        constructor = get_constructor_from_ergast_data(r['Constructor'])
        position = r['position']
        driver = get_driver_from_ergast_data(r['Driver'], constructor)

        qualifying_1 = None
        qualifying_2 = None
        qualifying_3 = None

        if 'Q1' in r:
            qualifying_1 = r['Q1']
        if 'Q2' in r:
            qualifying_1 = r['Q2']
        if 'Q3' in r:
            qualifying_1 = r['Q3']

        quali_res = QualifyingResult(position, driver, qualifying_1, qualifying_2, qualifying_3)
        quali_results.append(quali_res)

    return jsonify(SessionResultsGroup(date_time, quali_results).serialize())


def get_race_results(gp_round):
    response = requests.get(f'http://ergast.com/api/f1/current/{gp_round}/results.json')

    if response.status_code != 200:
        return jsonify({
            'error': f'api response code {response.status_code}'
        })

    result = response.json()['MRData']['RaceTable']['Races'][0]
    dt = result['date'] + ' ' + str(result['time']).replace('Z', '')
    date_time = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')

    qualifying = result['Results']

    race_results = []
    for i in range(len(qualifying)):
        r = qualifying[i]

        constructor = get_constructor_from_ergast_data(r['Constructor'])
        position = r['position']
        driver = get_driver_from_ergast_data(r['Driver'], constructor)

        status = r['status']
        points = r['points']
        fastest_lap = None

        if 'FastestLap' in r:
            rank = r['FastestLap']['rank']
            lap = r['FastestLap']['lap']
            time = r['FastestLap']['Time']['time']
            avg_speed = r['FastestLap']['AverageSpeed']
            fastest_lap = FastestLap(rank, lap, time, avg_speed)

        race_res = SessionResult(position, driver, status, points, fastest_lap)
        race_results.append(race_res)

    return jsonify(SessionResultsGroup(date_time, race_results).serialize())


def get_all_driver():
    response = requests.get('http://ergast.com/api/f1/current/driverStandings.json')
    if response.status_code != 200:
        return jsonify({
            'error': f'api response code {response.status_code}'
        })

    result = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    drivers = []
    for i in range(len(result)):
        d = result[i]
        constructor = get_constructor_from_ergast_data(d['Constructors'][0])
        driver = get_driver_from_ergast_data(d['Driver'], constructor)

        drivers.append(driver)

    return drivers


def get_driver_by_code(code):
    drivers = get_all_driver()

    for i in range(len(drivers)):
        d = drivers[i]
        if d.code == code:
            return d
