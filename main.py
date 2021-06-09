import json

from helpers import functions, fast_f1_helper
import fastf1 as ff1
from fastf1 import plotting

from flask import Flask, jsonify

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


if __name__ == '__main__':
    app.run(debug=True)
