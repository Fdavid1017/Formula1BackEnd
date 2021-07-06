import json

from fastf1.api import SessionNotAvailableError
from flask import make_response, Response, jsonify
from flask_restful import Resource, reqparse

from helpers.fast_f1_helper import get_car_data
from . import cache


class CarData(Resource):
    @cache.cached(timeout=600, query_string=True)
    def get(self, gp_name, session_type, driver):
        session_type = session_type.upper()
        driver = driver.upper()

        try:
            telemetry = get_car_data(gp_name, session_type, driver)
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

        telemetry = self.clean_up_data(telemetry)
        print(f'Returning {len(telemetry)} laps of data for {driver}')

        headers = {'Content-Type': 'application/json'}
        return make_response({'carData': self.telemetry_to_json(telemetry)}, 200, headers)

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
