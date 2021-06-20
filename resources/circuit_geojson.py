import json

from flask import jsonify
from flask_restful import Resource


class CircuitGeoJson(Resource):
    def get(self, geojson_map):
        with open(f'helpers/circuit/gjson_data/{geojson_map}') as f:
            data = json.load(f)

        return jsonify(data)
