from classes.color_scheme import ColorScheme
from classes.constructor import Constructor
from classes.driver import Driver
from classes.driver_standing import DriverStanding
from helpers.circuit.circuit_helper import load_json
from helpers.ergast_api_helper import get_all_driver


def get_constructor_color_scheme(constructor_id):
    json = load_json('helpers/constructor_color_scheme.json')
    colorSheme = ColorScheme(json[constructor_id]['primary'], json[constructor_id]['secondary'],
                             json[constructor_id]['tertiary'])

    return colorSheme


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
    color_scheme = get_constructor_color_scheme(constructor_id)

    return Constructor(constructor_id, name, color_scheme)


def get_driver_by_code(code):
    drivers = get_all_driver()

    for i in range(len(drivers)):
        d = drivers[i]
        if d.code == code:
            return d


def sort_by_constructor_standing(drivers, constructors, is_standing=False):
    constructor_position_map = {}

    for i in range(len(constructors)):
        c = constructors[i]
        constructor_position_map[c.constructor_id] = i

    new_drivers = []

    for d in drivers:
        key = None

        if is_standing:
            key = d.driver.constructor.constructor_id
        else:
            key = d.constructor.constructor_id

        position = constructor_position_map[key]
        new_d = d.__dict__
        new_d['constructor_position'] = position
        new_drivers.append(new_d)

    new_drivers.sort(key=lambda t: t['constructor_position'])
    drivers_list = []

    for t in new_drivers:
        driver = None

        if is_standing:
            d = t['driver']
            driver = Driver(d.driver_id, d.number, d.code, d.given_name, d.family_name, d.constructor)
            standing = DriverStanding(t['position'], t['points'], t['wins'], d)
            drivers_list.append(standing)
        else:
            d = t
            driver = Driver(d['driver_id'], d['number'], d['code'], d['given_name'], d['family_name'], d['constructor'])
            drivers_list.append(driver)

    return drivers_list
