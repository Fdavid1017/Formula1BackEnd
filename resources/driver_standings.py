import json

from flask import jsonify, Response
from flask_restful import Resource, reqparse

from exceptions.api_request_exception import ApiRequestException
from helpers.constructors_helper import get_all_constructor
from helpers.drivers_helper import get_drivers_standing
from helpers.functions import sort_by_constructor_standing


class DriverStandings(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('order', type=str, default='')

    def get(self):
        args = self.reqparse.parse_args()
        order_by = args['order']

        try:
            drivers = get_drivers_standing()
        except ApiRequestException as e:
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response

        if order_by == 'constructor':
            drivers = sort_by_constructor_standing(drivers, get_all_constructor(), True)

        for i in range(len(drivers)):
            drivers[i] = drivers[i].serialize()

        return jsonify(drivers)
