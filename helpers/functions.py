from classes.driver import Driver
from classes.driver_standing import DriverStanding


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
