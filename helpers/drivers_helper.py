import requests
from flask import jsonify

from classes.driver import Driver
from classes.driver_standing import DriverStanding
from exceptions.api_request_exception import ApiRequestException
from helpers.constructors_helper import get_constructor_from_ergast_data


def get_driver_by_code(code):
    drivers = get_all_driver()

    for i in range(len(drivers)):
        d = drivers[i]
        if d.code == code:
            return d


def get_driver_from_ergast_data(data, constructor):
    driver_id = data['driverId']
    driver_number = data['permanentNumber']
    code = data['code']
    given_name = data['givenName']
    family_name = data['familyName']

    return Driver(driver_id, driver_number, code, given_name, family_name, constructor)


def get_all_driver():
    response = requests.get('http://ergast.com/api/f1/current/driverStandings.json')

    if response.status_code != 200:
        raise ApiRequestException(f'Api responded with status code {response.status_code}')

    result = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    drivers = []
    for i in range(len(result)):
        d = result[i]
        constructor = get_constructor_from_ergast_data(d['Constructors'][0])
        driver = get_driver_from_ergast_data(d['Driver'], constructor)

        drivers.append(driver)

    return drivers


def get_drivers_standing():
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
        position = d['position']
        points = d['points']
        wins = d['wins']

        driver_standing = DriverStanding(position, points, wins, driver)
        drivers.append(driver_standing)

    return drivers
