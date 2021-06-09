import json

from helpers import functions, fast_f1_helper
import fastf1 as ff1
from fastf1 import plotting

from flask import Flask, jsonify, Blueprint

plotting.setup_mpl()
ff1.Cache.enable_cache('cache')

app = Flask(__name__)


@app.route('/api/get_schedule', methods=['GET'])
def get_schedule():
    return functions.get_schedule()


@app.route('/api/get_qualifying_results/<int:gp_round>', methods=['GET'])
def get_qualifying_results(gp_round):
    return functions.get_qualifying_results(gp_round)


@app.route('/api/get_race_results/<int:gp_round>', methods=['GET'])
def get_race_results(gp_round):
    return functions.get_race_results(gp_round)


@app.route('/api/get_free_practice_results/<string:gp_name>/<int:fp_number>', methods=['GET'])
def get_free_practice_results(gp_name, fp_number):
    session_type = 'FP1'

    if fp_number == 2:
        session_type = 'FP2'
    elif fp_number == 3:
        session_type = 'FP3'

    return jsonify(fast_f1_helper.get_fastest_laps_from_session(gp_name, session_type).serialize())


if __name__ == '__main__':
    app.run(debug=True)
