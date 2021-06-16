import json

from flask import jsonify, Response
from flask_restful import Resource

from exceptions.api_request_exception import ApiRequestException
from helpers.ergast_api_helper import get_teams_standing


class ConstructorStandings(Resource):
    def get(self):
        try:
            teams = get_teams_standing()
        except ApiRequestException as e:
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response

        for i in range(len(teams)):
            teams[i] = teams[i].serialize()

        return jsonify(teams)
