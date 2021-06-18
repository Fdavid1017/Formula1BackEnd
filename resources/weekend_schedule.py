import json

from flask import jsonify, Response
from flask_restful import Resource

from exceptions.api_request_exception import ApiRequestException
from exceptions.no_round_exception import NoRoundException
from helpers.ergast_api_helper import get_schedule_for_weekend


class WeekendSchedule(Resource):
    def get(self, gp_round):
        try:
            return jsonify(get_schedule_for_weekend(gp_round).serialize())
        except ApiRequestException as e:
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response
        except NoRoundException as e:
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response
