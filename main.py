import json

from flask_cors import cross_origin

from helpers import functions, fast_f1_helper
import fastf1 as ff1
from fastf1 import plotting

from flask import Flask, jsonify

plotting.setup_mpl()
ff1.Cache.enable_cache('cache')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/api/get_schedule', methods=['GET'])
@cross_origin()
def get_schedule():
    return jsonify(functions.get_schedule())


@app.route('/api/get_qualifying_results/<int:gp_round>', methods=['GET'])
@cross_origin()
def get_qualifying_results(gp_round):
    return jsonify(functions.get_qualifying_results(gp_round))


@app.route('/api/get_race_results/<int:gp_round>', methods=['GET'])
@cross_origin()
def get_race_results(gp_round):
    return jsonify(functions.get_race_results(gp_round))


@app.route('/api/get_free_practice_results/<string:gp_name>/<int:fp_number>', methods=['GET'])
@cross_origin()
def get_free_practice_results(gp_name, fp_number):
    session_type = 'FP1'

    if fp_number == 1:
        session_type = 'FP1'
    elif fp_number == 2:
        session_type = 'FP2'
    elif fp_number == 3:
        session_type = 'FP3'
    else:
        return jsonify({
            'error': f'No practice found with the practice number {fp_number}! Use values between 1-3'
        })

    return jsonify(fast_f1_helper.get_fastest_laps_from_session(gp_name, session_type).serialize())


@app.route('/api/get_all_driver', methods=['GET'], defaults={'order_by': None})
@app.route('/api/get_all_driver/<string:order_by>', methods=['GET'])
@cross_origin()
def get_all_driver(order_by):
    drivers = functions.get_all_driver()

    if order_by == 'name':
        drivers.sort(key=lambda d: d.given_name)
    elif order_by == 'constructor_standing':
        drivers = functions.sort_by_constructor_standing(drivers, functions.get_all_team())
    else:
        drivers.sort(key=lambda d: d.constructor.name)

    for i in range(len(drivers)):
        drivers[i] = drivers[i].serialize()

    return jsonify(drivers)


@app.route('/api/get_all_team', methods=['GET'], defaults={'order_by': None})
@app.route('/api/get_all_team/<string:order_by>', methods=['GET'])
@cross_origin()
def get_all_team(order_by):
    teams = functions.get_all_team()

    if order_by == 'name':
        teams.sort(key=lambda t: t.name)

    for i in range(len(teams)):
        teams[i] = teams[i].serialize()

    return jsonify(teams)


@app.route('/api/get_drivers_standing', methods=['GET'])
@cross_origin()
def get_drivers_standing():
    drivers = functions.get_drivers_standing()
    for i in range(len(drivers)):
        drivers[i] = drivers[i].serialize()

    return jsonify(drivers)


@app.route('/api/get_teams_standing', methods=['GET'])
@cross_origin()
def get_teams_standing():
    teams = functions.get_teams_standing()
    for i in range(len(teams)):
        teams[i] = teams[i].serialize()

    return jsonify(teams)


@app.route('/api/get_circuit_infos/<string:circuit_id>', methods=['GET'])
@cross_origin()
def get_circuit_infos(circuit_id):
    return jsonify(functions.get_circuit(circuit_id).serialize())


@app.route('/api/get_laps_for_session/<string:gp_name>/<string:session_type>/<string:return_format>', methods=['GET'])
@app.route('/api/get_laps_for_session/<string:gp_name>/<string:session_type>', methods=['GET'],
           defaults={'return_format': 'json'})
@cross_origin()
def get_laps_for_session(gp_name, session_type, return_format):
    laps = fast_f1_helper.get_laps(gp_name, session_type)

    laps = laps.drop(
        columns=['Stint', 'PitOutTime', 'PitInTime', 'Sector1SessionTime', 'Sector2SessionTime', 'Sector3SessionTime',
                 'FreshTyre', 'LapStartTime', 'IsAccurate'])
    print(f'Returning {len(laps.index)} row of telemetry data for the {gp_name} GP')
    if return_format == 'html':
        return laps.to_html()
    elif return_format == 'csv':
        return laps.to_csv()
    else:
        return laps.to_json()


@app.route(
    '/api/get_telemetry_for_session_and_driver/<string:gp_name>/<string:session_type>/<string:driver>/<string'
    ':return_format>',
    methods=['GET'])
@app.route('/api/get_telemetry_for_session_and_driver/<string:gp_name>/<string:session_type>/<string:driver>',
           methods=['GET'],
           defaults={'return_format': 'json'})
@cross_origin()
def get_telemetry_for_session_and_driver(gp_name, session_type, driver, return_format):
    telemetry = fast_f1_helper.get_telemetry(gp_name, session_type, driver)
    telemetry.fill_missing()
    telemetry = telemetry.drop(
        columns=['Date', 'DriverAhead', 'DistanceToDriverAhead', 'Source', 'Distance', 'Status', 'RelativeDistance'])
    print(f'Returning {len(telemetry.index)} row of telemetry data for {driver}')
    if return_format == 'html':
        return telemetry.to_html()
    elif return_format == 'csv':
        # USE CSV FOR SMALLEST SIZE AND FOR FASTER PROCESSING
        return telemetry.to_csv()
    elif return_format == 'string':
        return telemetry.to_string()
    else:
        return telemetry.to_json()


@app.route('/api/get_weather_for_session/<string:gp_name>/<string:session_type>/<string:return_format>',
           methods=['GET'])
@app.route('/api/get_weather_for_session/<string:gp_name>/<string:session_type>', methods=['GET'],
           defaults={'return_format': 'json'})
@cross_origin()
def get_weather_for_session(gp_name, session_type, return_format):
    weather = fast_f1_helper.get_weather(gp_name, session_type)
    weather = weather.drop(columns=['Humidity', 'Pressure', 'Rainfall'])
    print(f'Returning {len(weather.index)} row of weather data')
    if return_format == 'html':
        return weather.to_html()
    elif return_format == 'csv':
        # USE CSV FOR SMALLEST SIZE AND FOR FASTER PROCESSING
        return weather.to_csv()
    elif return_format == 'string':
        return weather.to_string()
    else:
        return weather.to_json()


@app.route('/api/get_tweets/<int:max_tweet>', methods=['GET'])
@app.route('/api/get_tweets', methods=['GET'], defaults={'max_tweet': 10})
@cross_origin()
def get_tweets(max_tweet):
    return functions.get_tweets(max_tweet)


if __name__ == '__main__':
    app.run(debug=True)
