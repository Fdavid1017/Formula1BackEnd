import requests

from classes.color_scheme import ColorScheme
from classes.constructor import Constructor
from classes.constructor_standing import ConstructorStanding
from exceptions.api_request_exception import ApiRequestException
from helpers.circuit.circuit_helper import load_json


def get_constructor_from_ergast_data(data):
    constructor_id = data['constructorId']
    name = data['name']
    color_scheme = get_constructor_color_scheme(constructor_id)

    return Constructor(constructor_id, name, color_scheme)


def get_constructor_color_scheme(constructor_id):
    json = load_json('helpers/constructor_color_scheme.json')
    colorSheme = ColorScheme(json[constructor_id]['primary'], json[constructor_id]['secondary'],
                             json[constructor_id]['tertiary'])

    return colorSheme


def get_all_constructor():
    response = requests.get('http://ergast.com/api/f1/current/constructorStandings.json')
    if response.status_code != 200:
        raise ApiRequestException(f'Api responded with status code {response.status_code}')

    result = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
    teams = []
    for i in range(len(result)):
        t = result[i]
        constructor = get_constructor_from_ergast_data(t['Constructor'])

        teams.append(constructor)

    return teams


def get_constructors_standing():
    response = requests.get('http://ergast.com/api/f1/current/constructorStandings.json')
    if response.status_code != 200:
        raise ApiRequestException(f'Api responded with status code {response.status_code}')

    result = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
    teams = []
    for i in range(len(result)):
        t = result[i]
        constructor = get_constructor_from_ergast_data(t['Constructor'])
        position = t['position']
        points = t['points']
        wins = t['wins']

        constructor_standing = ConstructorStanding(position, points, wins, constructor)

        teams.append(constructor_standing)

    return teams
