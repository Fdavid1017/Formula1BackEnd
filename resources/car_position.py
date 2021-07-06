import json

from fastf1.api import SessionNotAvailableError
from flask import Response, make_response
from flask_restful import Resource

from helpers.fast_f1_helper import get_car_position
from . import cache


class CarPosition(Resource):
    @cache.cached(timeout=600, query_string=True)
    def get(self, gp_name, session_type, driver):
        session_type = session_type.upper()
        driver = driver.upper()

        try:
            position_data = get_car_position(gp_name, session_type, driver)
        except SessionNotAvailableError as e:
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response
        except AttributeError as e:
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response
        except ValueError as e:
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response

        # position_data = self.clean_up_data(position_data)
        print(f'Returning {len(position_data)} laps of position data for {driver}')

        headers = {'Content-Type': 'application/json'}
        return make_response({'carData': self.telemetry_to_json(position_data)}, 200, headers)

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
