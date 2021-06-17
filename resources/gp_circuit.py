import json

from flask import jsonify, Response
from flask_restful import Resource

from exceptions.no_circuit_exception import NoCircuitException
from helpers.ergast_api_helper import get_circuit_for_gp


class GpCircuit(Resource):
    def get(self, gp_round):
        try:
            return jsonify(get_circuit_for_gp(gp_round).serialize())
        except NoCircuitException as e:
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response
