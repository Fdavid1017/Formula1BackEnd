import json

from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from helpers.telemetry_to_json import telemetry_to_json
from . import cache

from helpers.drivers_helper import get_all_driver
from helpers.fast_f1_helper import get_car_data


class AllCarData(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from', type=int, default=0)
        self.reqparse.add_argument('till', type=int, default=0)

    @cache.cached(timeout=600, query_string=True)
    def get(self, gp_name, session_type):
        args = self.reqparse.parse_args()
        from_lap = args['from']
        till_lap = args['till']

        session_type = session_type.upper()
        drivers = get_all_driver()

        driversLaps = {}
        for i in range(len(drivers)):
            driver = drivers[i]
            print(f'Getting data for {driver.code} in {gp_name} {session_type}')
            laps_data = get_car_data(gp_name, session_type, driver.code, from_lap, till_lap)

            laps_data = telemetry_to_json(laps_data)
            driversLaps[driver.code] = laps_data

        headers = {'Content-Type': 'application/json'}
        return make_response(json.dumps({'carsData': driversLaps}, separators=(',', ':')), 200, headers)

    def clean_up_data(self, telemetry):
        for i in range(len(telemetry)):
            telemetry[i] = telemetry[i].drop(
                columns=['Date', 'DriverAhead', 'DistanceToDriverAhead', 'Source', 'Distance', 'Status',
                         'RelativeDistance'], errors='ignore')

        return telemetry
