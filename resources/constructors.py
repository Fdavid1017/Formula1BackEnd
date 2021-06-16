import json

from flask import jsonify, Response
from flask_restful import Resource, reqparse

from exceptions.api_request_exception import ApiRequestException
from helpers.functions import get_all_team


class Constructors(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('order', type=str, default='')

    def get(self):
        args = self.reqparse.parse_args()
        order_by = args['order']

        try:
            teams = get_all_team()
        except ApiRequestException as e:
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response

        if order_by == 'name':
            teams.sort(key=lambda t: t.name)

        for i in range(len(teams)):
            teams[i] = teams[i].serialize()
        return jsonify(teams)
