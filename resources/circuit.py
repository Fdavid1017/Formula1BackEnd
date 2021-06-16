import json

from flask import jsonify, Response
from flask_restful import Resource

from exceptions.no_circuit_exception import NoCircuitException
from helpers.functions import get_circuit


class Circuit(Resource):
    def get(self, circuit_id):
        try:
            return jsonify(get_circuit(circuit_id).serialize())
        except NoCircuitException as e:
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response
