import json

from flask import Response, make_response
from flask_restful import Resource, reqparse

from helpers.fast_f1_helper import get_laps


class Laps(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('format', type=str, default='')

    def get(self, gp_name, session_type):
        args = self.reqparse.parse_args()
        return_format = args['format']

        allowed_session_types = [
            'R', 'Q', 'FP1', 'FP2', 'FP3'
        ]
        session_type = session_type.upper()

        if session_type not in allowed_session_types:
            print(f'Not allowed session type: {session_type}')
            response = Response(
                response=json.dumps({'error': f'Not allowed session type: {session_type}'}),
                status=500, mimetype='application/json')
            return response

        laps = get_laps(gp_name, session_type)

        laps = laps.drop(
            columns=['Stint', 'PitOutTime', 'PitInTime', 'Sector1SessionTime', 'Sector2SessionTime',
                     'Sector3SessionTime',
                     'FreshTyre', 'LapStartTime', 'IsAccurate'])

        print(f'Returning {len(laps.index)} row of lap data for the {gp_name} GP')

        if return_format == 'html':
            headers = {'Content-Type': 'text/html'}
            return make_response(laps.to_html(), 200, headers)
        elif return_format == 'csv':
            headers = {}
            return make_response(laps.to_csv(), 200, headers)
        else:
            headers = {'Content-Type': 'application/json'}
            return make_response(laps.to_json(date_unit='ms'), 200, headers)
