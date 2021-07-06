from flask import make_response
from flask_restful import Resource
from . import cache

from helpers.drivers_helper import get_all_driver
from helpers.fast_f1_helper import get_car_position


class AllCarPosition(Resource):
    @cache.cached(timeout=600, query_string=True)
    def get(self, gp_name, session_type):
        session_type = session_type.upper()
        drivers = get_all_driver()

        driversLaps = {}
        for i in range(len(drivers)):
            driver = drivers[i]
            print(f'Getting data for {driver.code} in {gp_name} {session_type}')
            lapsData = get_car_position(gp_name, session_type, driver.code)
            lapsData = self.telemetry_to_json(lapsData)
            driversLaps[driver.code] = lapsData

        headers = {'Content-Type': 'application/json'}
        return make_response({'carsData': driversLaps}, 200, headers)

    def telemetry_to_json(self, telemetry):
        jsonData = []
        for i in range(len(telemetry)):
            tel = telemetry[i]
            data = {}

            if 'Date' in tel.columns:
                data["Date"] = tel['Date'].tolist()

            if 'X' in tel.columns:
                data["X"] = tel['X'].tolist()

            if 'Y' in tel.columns:
                data["Y"] = tel['Y'].tolist()

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
