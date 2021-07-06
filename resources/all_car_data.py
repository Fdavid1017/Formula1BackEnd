import json

from flask import jsonify, make_response
from flask_restful import Resource, reqparse
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
            laps_data = get_car_data(gp_name, session_type, driver.code)

            if till_lap > 0 and from_lap < till_lap:
                laps_data = laps_data[from_lap:till_lap + 1]

            laps_data = self.telemetry_to_json(laps_data)
            driversLaps[driver.code] = laps_data

        headers = {'Content-Type': 'application/json'}
        return make_response(json.dumps({'carsData': driversLaps}, separators=(',', ':')), 200, headers)

    def clean_up_data(self, telemetry):
        for i in range(len(telemetry)):
            telemetry[i] = telemetry[i].drop(
                columns=['Date', 'DriverAhead', 'DistanceToDriverAhead', 'Source', 'Distance', 'Status',
                         'RelativeDistance'], errors='ignore')

        return telemetry

    def telemetry_to_json(self, telemetry):
        jsonData = []
        for i in range(len(telemetry)):
            tel = telemetry[i]
            data = {}

            if 'RPM' in tel.columns:
                data["RPM"] = tel['RPM'].tolist()

            if 'Speed' in tel.columns:
                data["Speed"] = tel['Speed'].tolist()

            if 'nGear' in tel.columns:
                data["nGear"] = tel['nGear'].tolist()

            if 'Throttle' in tel.columns:
                data["Throttle"] = tel['Throttle'].tolist()

            if 'Brake' in tel.columns:
                data["Brake"] = tel['Brake'].tolist()

            if 'DRS' in tel.columns:
                data["DRS"] = tel['DRS'].tolist()

            if 'Time' in tel.columns:
                data["Time"] = tel['Time'].tolist()
                for k in range(len(data["Time"])):
                    data["Time"][k] = str(data["Time"][k])

            if 'SessionTime' in tel.columns:
                data["SessionTime"] = tel['SessionTime'].tolist()
                for k in range(len(data["SessionTime"])):
                    data["SessionTime"][k] = str(data["SessionTime"][k])

            jsonData.append(data)

        return jsonData
