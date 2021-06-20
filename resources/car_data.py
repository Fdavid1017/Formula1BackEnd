import json

from fastf1.api import SessionNotAvailableError
from flask import make_response, Response, jsonify
from flask_restful import Resource, reqparse

from helpers.fast_f1_helper import get_car_data


class CarData(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('format', type=str, default='')

    def get(self, gp_name, session_type, driver):
        args = self.reqparse.parse_args()
        return_format = args['format']

        session_type = session_type.upper()
        driver = driver.upper()

        try:
            telemetry = get_car_data(gp_name, session_type, driver)
        except SessionNotAvailableError as e:
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response
        except AttributeError as e:
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response
        except ValueError as e:
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response

        # telemetry = telemetry.drop(
        #     columns=['Date', 'DriverAhead', 'DistanceToDriverAhead', 'Source', 'Distance', 'Status',
        #              'RelativeDistance'], errors='ignore')

        # print(f'Returning {len(telemetry.index)} row of telemetry data for {driver}')

        telemetry = self.clean_up_data(telemetry)
        print(f'Returning {len(telemetry)} laps of data for {driver}')

        headers = {'Content-Type': 'application/json'}
        return make_response({'carData': self.telemetry_to_json(telemetry)}, 200, headers)
        # return jsonify(self.telemetry_to_json(telemetry))

        # if return_format == 'html':
        #     headers = {'Content-Type': 'text/html'}
        #     return make_response(telemetry.to_html(), 200, headers)
        # elif return_format == 'csv':
        #     # USE CSV FOR SMALLEST SIZE AND FOR FASTER PROCESSING
        #     headers = {'Content-Type': 'text/csv'}
        #     return make_response(telemetry.to_csv(), 200, headers)
        # elif return_format == 'string':
        #     return telemetry.to_string()
        # else:
        #     headers = {'Content-Type': 'application/json'}
        #     return make_response(telemetry.to_json(), 200, headers)

    def clean_up_data(self, telemetry):
        for i in range(len(telemetry)):
            telemetry[i] = telemetry[i].drop(
                columns=['Date', 'DriverAhead', 'DistanceToDriverAhead', 'Source', 'Distance', 'Status',
                         'RelativeDistance'], errors='ignore')

        return telemetry

    def telemetry_to_json(self, telemetry):
        jsonData = []
        for i in range(len(telemetry)):
            tel = telemetry[i]
            data = {}

            if 'RPM' in tel.columns:
                data["RPM"] = tel['RPM'].tolist()

            if 'Speed' in tel.columns:
                data["Speed"] = tel['Speed'].tolist()

            if 'nGear' in tel.columns:
                data["nGear"] = tel['nGear'].tolist()

            if 'Throttle' in tel.columns:
                data["Throttle"] = tel['Throttle'].tolist()

            if 'Brake' in tel.columns:
                data["Brake"] = tel['Brake'].tolist()

            if 'DRS' in tel.columns:
                data["DRS"] = tel['DRS'].tolist()

            if 'Time' in tel.columns:
                data["Time"] = tel['Time'].tolist()
                for k in range(len(data["Time"])):
                    data["Time"][k] = str(data["Time"][k])

            if 'SessionTime' in tel.columns:
                data["SessionTime"] = tel['SessionTime'].tolist()
                for k in range(len(data["SessionTime"])):
                    data["SessionTime"][k] = str(data["SessionTime"][k])

            jsonData.append(data)

            # try:
            #     print(
            #         f'{i}:\n\tRPM: {len(data["RPM"])}\n\tSpeed: {len(data["Speed"])}\n\tnGear: {len(data["nGear"])}'
            #         f'\n\tThrottle: {len(data["Throttle"])}'
            #         f'\n\tBrake: {len(data["Brake"])}\n\tDRS: {len(data["DRS"])}'
            #         f'\n\tTime: {len(data["Time"])}\n\tSessionTime: {len(data["SessionTime"])}')
            # except:
            #     print('Error')
            #
            # print()
            # print()

        # print('Col names:')
        # for col in telemetry[1].columns:
        #     print(col)
        return jsonData
