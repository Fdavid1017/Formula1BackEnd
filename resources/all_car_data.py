import time

from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from helpers.load_laps import LoadLaps
from helpers.telemetry_to_json import telemetry_to_json
from . import cache

from helpers.drivers_helper import get_all_driver


class AllCarData(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from', type=int, default=0)
        self.reqparse.add_argument('till', type=int, default=0)

    @cache.cached(timeout=600, query_string=True)
    def get(self, gp_name, session_type):
        # args = self.reqparse.parse_args()
        # from_lap = args['from']
        # till_lap = args['till']
        #
        # session_type = session_type.upper()
        # drivers = get_all_driver()
        #
        # driversLaps = {}
        # for i in range(len(drivers)):
        #     driver = drivers[i]
        #     print(f'Getting data for {driver.code} in {gp_name} {session_type}')
        #     laps_data = get_car_data(gp_name, session_type, driver.code, from_lap, till_lap)
        #
        #     laps_data = telemetry_to_json(laps_data)
        #     driversLaps[driver.code] = laps_data
        #
        # headers = {'Content-Type': 'application/json'}
        # return make_response(json.dumps({'carsData': driversLaps}, separators=(',', ':')), 200, headers)
        # args = self.reqparse.parse_args()
        # from_lap = args['from']
        # till_lap = args['till']
        session_type = session_type.upper()

        tic = time.perf_counter()

        drivers = get_all_driver()
        load_laps = LoadLaps()
        laps = load_laps.load_laps_with_telemetry(gp_name, session_type)

        drivers_positions_data = {}
        for i in range(len(drivers)):
            driver = drivers[i]
            print(f'Getting data for {driver.code} in {gp_name} {session_type}')
            driver_laps = laps.pick_driver(driver.code)

            # for k in range(len(driver_laps.columns)):
            #     print(driver_laps.columns[k])

            try:
                tel = driver_laps.get_car_data()

                # print()
                # for k in range(len(tel.columns)):
                #     print(tel.columns[k])

                tel = tel.add_distance()
                tel['Compound'] = driver_laps['Compound']
                tel['TyreLife'] = driver_laps['TyreLife']
                tel['TrackStatus'] = driver_laps['TrackStatus']

                # data = driver_laps.get_pos_data()
                drivers_positions_data[driver.code] = telemetry_to_json(tel)
            except ValueError as e:
                print(e)

        toc = time.perf_counter()
        print(f"Data received in {toc - tic:0.4f} seconds")
        return jsonify(drivers_positions_data)
