import json

from flask import jsonify, Response
from flask_restful import Resource

from exceptions.api_request_exception import ApiRequestException
from helpers.functions import get_schedule


class Schedule(Resource):
    def get(self):
        try:
            return jsonify(get_schedule())
        except ApiRequestException as e:
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response
