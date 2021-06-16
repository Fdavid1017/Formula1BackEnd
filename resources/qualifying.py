import json

from flask import jsonify, Response
from flask_restful import Resource

from exceptions.no_round_exception import NoRoundException
from helpers.ergast_api_helper import get_qualifying_results


class Qualifying(Resource):
    def get(self, gp_round):
        try:
            result = get_qualifying_results(gp_round).serialize()
            return jsonify(result)
        except NoRoundException as e:
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=404, mimetype='application/json')
            return response
