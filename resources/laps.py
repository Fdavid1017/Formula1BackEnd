import json

from flask import Response
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

        print(f'Returning {len(laps.index)} row of telemetry data for the {gp_name} GP')

        if return_format == 'html':
            return laps.to_html()
        elif return_format == 'csv':
            return laps.to_csv()
        else:
            return laps.to_json()
