import json


def load_json(file_location):
    f = open(file_location)
    data = json.load(f)
    return data


def get_circuit(json, circuit_id):
    for i in range(len(json)):
        if json[i]['circuit_id'] == circuit_id:
            return json[i]
