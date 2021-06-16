import json

from fastf1.api import SessionNotAvailableError
from flask import jsonify, Response
from flask_restful import Resource

from exceptions.invalid_practice_number_exception import InvalidPracticeNumberException
from helpers.fast_f1_helper import get_fastest_laps_from_session


class Practice(Resource):
    def get(self, gp_name, fp_number):
        session_type = 'FP1'

        try:
            if fp_number == 1:
                session_type = 'FP1'
            elif fp_number == 2:
                session_type = 'FP2'
            elif fp_number == 3:
                session_type = 'FP3'
            else:
                raise InvalidPracticeNumberException(f'Invalid practice number {fp_number}! Must be between 1-3')
        except InvalidPracticeNumberException as e:
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response

        try:
            return jsonify(get_fastest_laps_from_session(gp_name, session_type).serialize())
        except SessionNotAvailableError as e:
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=404, mimetype='application/json')
            return response
