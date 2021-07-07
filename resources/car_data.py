import json

from fastf1.api import SessionNotAvailableError
from flask import make_response, Response, jsonify
from flask_restful import Resource, reqparse

from helpers.fast_f1_helper import get_car_data
from helpers.telemetry_to_json import telemetry_to_json
from . import cache


class CarData(Resource):
    @cache.cached(timeout=18000, query_string=True)
    def get(self, gp_name, session_type, driver):
        session_type = session_type.upper()
        driver = driver.upper()

        try:
            telemetry = get_car_data(gp_name, session_type, driver)
        except SessionNotAvailableError as e:
            print('SessionNotAvailableError')
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response
        except AttributeError as e:
            print('AttributeError')
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response
        except ValueError as e:
            print('ValueError')
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response

        telemetry = self.clean_up_data(telemetry)
        print(f'Returning {len(telemetry)} laps of data for {driver}')

        headers = {'Content-Type': 'application/json'}
        return make_response({'carData': telemetry_to_json(telemetry)}, 200, headers)

    def clean_up_data(self, telemetry):
        for i in range(len(telemetry)):
            telemetry[i] = telemetry[i].drop(
                columns=['Date', 'DriverAhead', 'DistanceToDriverAhead', 'Source', 'Distance', 'Status',
                         'RelativeDistance'], errors='ignore')

        return telemetry
