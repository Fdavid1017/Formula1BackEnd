import json

from fastf1.api import SessionNotAvailableError
from flask import Response, make_response
from flask_restful import Resource, reqparse

from helpers.fast_f1_helper import get_weather


class Weather(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('format', type=str, default='')

    def get(self, gp_name, session_type):
        args = self.reqparse.parse_args()
        return_format = args['format']
        session_type = session_type.upper()

        try:
            weather = get_weather(gp_name, session_type)
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

        weather = weather.drop(columns=['Humidity', 'Pressure', 'Rainfall'], errors='ignore')
        print(f'Returning {len(weather.index)} row of weather data for {gp_name} {session_type}')
        if return_format == 'html':
            headers = {'Content-Type': 'application/html'}
            return make_response(weather.to_html(), 200, headers)
        elif return_format == 'csv':
            # USE CSV FOR SMALLEST SIZE AND FOR FASTER PROCESSING
            headers = {'Content-Type': 'application/csv'}
            return make_response( weather.to_csv(), 200, headers)
        elif return_format == 'string':
            return weather.to_string()
        else:
            headers = {'Content-Type': 'application/json'}
            return make_response(weather.to_json(), 200, headers)
