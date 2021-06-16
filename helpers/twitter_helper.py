import requests

from exceptions.api_request_exception import ApiRequestException

previous_token = None
my_twitter_bearier_code = 'AAAAAAAAAAAAAAAAAAAAADMCQgEAAAAAxhXAjDGboVXagHd5QH9c5jra5%2Bo%3DI3yZvEbd35XF6dJnX1fhNq0d3dO4mgVIv41lAUoaix79V7yZ3Y'


def get_tweets(max_results=None):
    global previous_token

    headers = {"Authorization": f"Bearer {my_twitter_bearier_code}"}
    params = {}

    print(max_results)

    if max_results is not None:
        params['max_results'] = max_results

    response = requests.get(f'https://api.twitter.com/2/users/69008563/tweets', params=params, headers=headers)
    if response.status_code != 200:
        raise ApiRequestException(f'Api returned with status code {response.status_code}')

    result = response.json()
    previous_token = result['meta']['next_token']

    return result['data']


def get_next_tweets(max_results=None):
    global previous_token

    headers = {"Authorization": f"Bearer {my_twitter_bearier_code}"}
    params = {}

    if max_results is not None:
        params['max_results'] = max_results

    if previous_token is not None:
        params['pagination_token'] = previous_token

    response = requests.get(f'https://api.twitter.com/2/users/69008563/tweets', params=params, headers=headers)
    if response.status_code != 200:
        raise ApiRequestException(f'Api returned with status code {response.status_code}')

    result = response.json()
    previous_token = result['meta']['next_token']

    return result['data']


def reset_tweets():
    global previous_token
    previous_token = None
