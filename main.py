from flask import Flask, jsonify
import requests
from datetime import datetime

from classes.circuit import Circuit
from classes.color_scheme import ColorScheme
from classes.race import Race
from helpers.circuit.circuit_helper import load_json, get_circuit

app = Flask(__name__)


@app.route('/api/get_all_races')
def get_all_races():
    response = requests.get('http://ergast.com/api/f1/current.json')

    if response.status_code == 200:
        result = response.json()['MRData']['RaceTable']['Races']

        races = []
        for i in range(len(result)):
            r = result[i]

            # Race properties
            race_round = r['round']
            race_name = r['raceName']
            dt = r['date'] + ' ' + str(r['time']).replace('Z', '')
            date_time = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')

            # Circuit properties

            circuit_json = load_json('helpers/circuit/circuits.json')

            c = r['Circuit']

            current_c = get_circuit(circuit_json, c['circuitId'])

            circuit_id = c['circuitId']
            circuit_name = c['circuitName']
            city = c['Location']['locality']
            country = c['Location']['country']
            image_location = current_c['image_location']
            first_gp = current_c['first_gp']
            number_of_laps = current_c['number_of_laps']
            length = current_c['length']
            race_distance = current_c['race_distance']
            gjson_map = current_c['gjson_map']
            color_scheme = ColorScheme(current_c['primary_color'], current_c['secondary'], current_c['tertiary'])

            circuit = Circuit(circuit_id, circuit_name, city, country, image_location, first_gp, number_of_laps, length,
                              race_distance, gjson_map, color_scheme)

            race = Race(race_round, race_name, circuit, date_time)
            races.append(race.serialize())

        return jsonify(races)
    else:
        return jsonify({
            'error': f'api response code {response.status_code}'
        })


if __name__ == '__main__':
    app.run(debug=True)
