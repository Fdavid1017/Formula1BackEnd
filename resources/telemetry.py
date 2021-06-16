from flask_restful import Resource, reqparse

from helpers.fast_f1_helper import get_telemetry


class Telemetry(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('format', type=str, default='')

    def get(self, gp_name, session_type, driver):
        args = self.reqparse.parse_args()
        return_format = args['format']

        session_type = session_type.upper()
        driver = driver.upper()

        telemetry = get_telemetry(gp_name, session_type, driver)
        # telemetry.fill_missing()
        telemetry = telemetry.drop(
            columns=['Date', 'DriverAhead', 'DistanceToDriverAhead', 'Source', 'Distance', 'Status',
                     'RelativeDistance'])
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
