import fastf1 as ff1
from fastf1 import plotting
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

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
from resources.telemetry import Telemetry
# Fast F1 setup
from resources.tweets import Tweets
from resources.weather import Weather

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
api.add_resource(Telemetry, '/api/telemetry/<string:gp_name>/<string:session_type>/<string:driver>',
                 endpoint="telemetry")
api.add_resource(Weather, '/api/weather/<string:gp_name>/<string:session_type>', endpoint="weather")

if __name__ == '__main__':
    app.run(debug=True)
