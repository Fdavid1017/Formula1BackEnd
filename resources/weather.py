from flask_restful import Resource, reqparse

from helpers.fast_f1_helper import get_weather


class Weather(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('format', type=str, default='')

    def get(self, gp_name, session_type):
        args = self.reqparse.parse_args()
        return_format = args['format']
        session_type = session_type.upper()

        weather = get_weather(gp_name, session_type)
        weather = weather.drop(columns=['Humidity', 'Pressure', 'Rainfall'], errors='ignore')
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
