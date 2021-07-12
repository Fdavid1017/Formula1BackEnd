import requests

from exceptions.api_request_exception import ApiRequestException

my_twitter_bearier_code = 'AAAAAAAAAAAAAAAAAAAAADMCQgEAAAAAxhXAjDGboVXagHd5QH9c5jra5%2Bo%3DI3yZvEbd35XF6dJnX1fhNq0d3dO4mgVIv41lAUoaix79V7yZ3Y'


def get_tweets(max_results=None, pagination_token=None):
    headers = {
        "Authorization": f"Bearer {my_twitter_bearier_code}",
        'Cache - Control': 'no - cache'
    }
    params = {}

    if max_results is not None:
        params['max_results'] = max_results

    if pagination_token is not None:
        params['pagination_token'] = pagination_token

    response = requests.get(
        f'https://api.twitter.com/2/users/69008563/tweets?tweet.fields=attachments,created_at,entities,geo,id,in_reply_to_user_id,referenced_tweets,text,withheld&expansions=referenced_tweets.id,attachments.media_keys&media.fields=media_key,type,url',
        params=params, headers=headers)
    if response.status_code != 200:
        raise ApiRequestException(f'Api returned with status code {response.status_code}')

    result = response.json()

    data = result['data']
    for data_index in range(len(data)):
        if 'entities' in data[data_index] and 'urls' in data[data_index]['entities']:
            for url_index in range(len(data[data_index]['entities']['urls'])):
                if data[data_index]['entities']['urls'][url_index]['display_url'].startswith('pic.twitter.com') and len(
                        data[data_index]['attachments']['media_keys']) > url_index:
                    media_key = data[data_index]['attachments']['media_keys'][url_index]
                    media_index = next(
                        (i for i, item in enumerate(result['includes']['media']) if
                         item['media_key'] == media_key and item['type'] == 'photo'), -1)

                    if media_index > -1:
                        data[data_index]['entities']['urls'][url_index]['image_url'] = \
                            result['includes']['media'][media_index]['url']

    rsp = {
        'data': data,
        'next_token': result['meta']['next_token']
    }

    return rsp
