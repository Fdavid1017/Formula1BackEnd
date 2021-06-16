import json

from flask import jsonify, Response
from flask_restful import Resource, reqparse

from exceptions.api_request_exception import ApiRequestException
from helpers.functions import get_all_driver, sort_by_constructor_standing, get_all_team


class Drivers(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('order', type=str, default='')

    def get(self):
        args = self.reqparse.parse_args()
        order_by = args['order']

        try:
            drivers = get_all_driver()
        except ApiRequestException as e:
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response

        if order_by == 'name':
            drivers.sort(key=lambda d: d.given_name)
        elif order_by == 'constructor':
            drivers = sort_by_constructor_standing(drivers, get_all_team())
        else:
            drivers.sort(key=lambda d: d.constructor.name)

        for i in range(len(drivers)):
            drivers[i] = drivers[i].serialize()

        return jsonify(drivers)
