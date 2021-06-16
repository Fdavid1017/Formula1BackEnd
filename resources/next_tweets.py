import json

from flask import Response, jsonify
from flask_restful import Resource, reqparse

from exceptions.api_request_exception import ApiRequestException
from helpers.twitter_helper import get_next_tweets


class NextTweets(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('max_results', type=str, default=None)

    def get(self):
        args = self.reqparse.parse_args()
        max_results = args['max_results']

        try:
            result = get_next_tweets(max_results)
        except ApiRequestException as e:
            print(e)
            response = Response(
                response=json.dumps({'error': str(e)}),
                status=500, mimetype='application/json')
            return response

        return jsonify(result)
