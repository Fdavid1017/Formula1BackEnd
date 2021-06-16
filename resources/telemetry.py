import json

from fastf1.api import SessionNotAvailableError
from flask import Response
from flask_restful import Resource, reqparse

from helpers.fast_f1_helper import get_telemetry


class Telemetry(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('format', type=str, default='')

    def get(self, gp_name, session_type, driver):
        args = self.reqparse.parse_args()
        return_format = args['format']

        session_type = session_type.upper()
        driver = driver.upper()

        try:
            telemetry = get_telemetry(gp_name, session_type, driver)
            telemetry.fill_missing()
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

        # if 'Date' in telemetry.columns:
        #     telemetry = telemetry.drop(columns=['Date'])
        #
        # if 'DriverAhead' in telemetry.columns:
        #     telemetry = telemetry.drop(columns=['DriverAhead'])
        #
        # if 'DistanceToDriverAhead' in telemetry.columns:
        #     telemetry = telemetry.drop(columns=['DistanceToDriverAhead'])
        #
        # if 'Source' in telemetry.columns:
        #     telemetry = telemetry.drop(columns=['Source'])
        #
        # if 'Distance' in telemetry.columns:
        #     telemetry = telemetry.drop(columns=['Distance'])
        #
        # if 'Status' in telemetry.columns:
        #     telemetry = telemetry.drop(columns=['Status'])
        #
        # if 'RelativeDistance' in telemetry.columns:
        #     telemetry = telemetry.drop(columns=['RelativeDistance'])

        telemetry = telemetry.drop(
            columns=['Date', 'DriverAhead', 'DistanceToDriverAhead', 'Source', 'Distance', 'Status',
                     'RelativeDistance'], errors='ignore')
        print(f'Returning {len(telemetry.index)} row of telemetry data for {driver}')

        if return_format == 'html':
            return telemetry.to_html()
        elif return_format == 'csv':
            # USE CSV FOR SMALLEST SIZE AND FOR FASTER PROCESSING
            return telemetry.to_csv()
        elif return_format == 'string':
            return telemetry.to_string()
        else:
            return telemetry.to_json()
