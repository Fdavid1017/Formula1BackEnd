import fastf1 as ff1
from fastf1 import plotting

from flask import Flask
from flask_restful import Api

from helpers import fast_f1_helper, functions
from resources.circuit import Circuit
from resources.constructor_standings import ConstructorStandings
from resources.constructors import Constructors
from resources.driver_standings import DriverStandings
from resources.drivers import Drivers
from resources.laps import Laps
from resources.next_tweets import NextTweets
from resources.practice import Practice
from resources.qualifying import Qualifying
from resources.race import Race
from resources.schedule import Schedule
from flask_cors import CORS, cross_origin

from resources.telemetry import Telemetry

# Fast F1 setup
from resources.tweets import Tweets

plotting.setup_mpl()
ff1.Cache.enable_cache('cache')

# Flask & Flask Restfull setup
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

api.add_resource(Schedule, '/api/schedules', endpoint="schedulea")
api.add_resource(Qualifying, '/api/qualifying/<int:gp_round>', endpoint="qualifying_by_round")
api.add_resource(Race, '/api/races/<int:gp_round>', endpoint="races_by_round")
api.add_resource(Practice, '/api/practices/<string:gp_name>/<int:fp_number>', endpoint="practices_by_name_and_number")
api.add_resource(Drivers, '/api/drivers', endpoint="drivers")
api.add_resource(Constructors, '/api/constructors', endpoint="constructors")
api.add_resource(DriverStandings, '/api/driverStandings', endpoint="driver_standings")
api.add_resource(ConstructorStandings, '/api/constructorStandings', endpoint="constructor_standings")
api.add_resource(Circuit, '/api/circuit/<string:circuit_id>', endpoint="circuit")
api.add_resource(Laps, '/api/laps/<string:gp_name>/<string:session_type>', endpoint="laps")
api.add_resource(Tweets, '/api/tweets', endpoint="tweets")
api.add_resource(NextTweets, '/api/next_tweets', endpoint="next_tweets")
# api.add_resource(Telemetry, '/api/telemetry/<string:gp_name>/<string:session_type>/<string:driver>',
#                  endpoint="telemetry")

# @app.route(
#     '/api/get_telemetry_for_session_and_driver/<string:gp_name>/<string:session_type>/<string:driver>/<string'
#     ':return_format>',
#     methods=['GET'])
# @app.route('/api/get_telemetry_for_session_and_driver/<string:gp_name>/<string:session_type>/<string:driver>',
#            methods=['GET'],
#            defaults={'return_format': 'json'})
# @cross_origin()
# def get_telemetry_for_session_and_driver(gp_name, session_type, driver, return_format):
#     telemetry = fast_f1_helper.get_telemetry(gp_name, session_type, driver)
#     telemetry.fill_missing()
#     telemetry = telemetry.drop(
#         columns=['Date', 'DriverAhead', 'DistanceToDriverAhead', 'Source', 'Distance', 'Status', 'RelativeDistance'])
#     print(f'Returning {len(telemetry.index)} row of telemetry data for {driver}')
#     if return_format == 'html':
#         return telemetry.to_html()
#     elif return_format == 'csv':
#         # USE CSV FOR SMALLEST SIZE AND FOR FASTER PROCESSING
#         return telemetry.to_csv()
#     elif return_format == 'string':
#         return telemetry.to_string()
#     else:
#         return telemetry.to_json()
#
#
# @app.route('/api/get_weather_for_session/<string:gp_name>/<string:session_type>/<string:return_format>',
#            methods=['GET'])
# @app.route('/api/get_weather_for_session/<string:gp_name>/<string:session_type>', methods=['GET'],
#            defaults={'return_format': 'json'})
# @cross_origin()
# def get_weather_for_session(gp_name, session_type, return_format):
#     weather = fast_f1_helper.get_weather(gp_name, session_type)
#     weather = weather.drop(columns=['Humidity', 'Pressure', 'Rainfall'])
#     print(f'Returning {len(weather.index)} row of weather data')
#     if return_format == 'html':
#         return weather.to_html()
#     elif return_format == 'csv':
#         # USE CSV FOR SMALLEST SIZE AND FOR FASTER PROCESSING
#         return weather.to_csv()
#     elif return_format == 'string':
#         return weather.to_string()
#     else:
#         return weather.to_json()

if __name__ == '__main__':
    app.run(debug=True)
