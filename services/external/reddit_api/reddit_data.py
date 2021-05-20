import pandas
import requests

from services.external.reddit_api.secrets import REDDIT_USERNAME, REDDIT_PASSWORD, CLIENT_ID, SECRET_KEY


# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'


def get_hot_posts(topic, limit=25):
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
    topic = topic.lower()
    # here we pass our login method (password), username, and password
    data = {'grant_type': 'password',
            'username': REDDIT_USERNAME,
            'password': REDDIT_PASSWORD}

    # setup our header info, which gives reddit_api a brief description of our app
    headers = {'User-Agent': 'ReDatAPI v0.0.1'}

    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    # convert response to JSON and pull access_token value
    token = res.json()['access_token']

    # add authorization to our headers dictionary
    headers['Authorization'] = f"bearer {token}"

    # while the token is valid (~2 hours) we just add headers=headers to our requests
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    res = requests.get('https://oauth.reddit.com/r/{topic}/hot'.format(topic=topic), headers=headers,
                       params={'limit': '{limit}'.format(limit=limit)})

    posts = []
    for post in res.json()['data']['children']:
        posts.append(post)
    # print(post['data'].keys())  # items that can be obtained
    return posts


def get_trending_subreddits(limit=25, before=None):
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

    # here we pass our login method (password), username, and password
    data = {'grant_type': 'password',
            'username': REDDIT_USERNAME,
            'password': REDDIT_PASSWORD}

    # setup our header info, which gives reddit_api a brief description of our app
    headers = {'User-Agent': 'ReDatAPI v0.0.1'}

    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    # convert response to JSON and pull access_token value
    token = res.json()['access_token']

    # add authorization to our headers dictionary
    headers['Authorization'] = f"bearer {token}"

    # while the token is valid (~2 hours) we just add headers=headers to our requests
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    res = requests.get('https://oauth.reddit.com/r/trending_subreddits', headers=headers,
                       params={'limit': '{limit}'.format(limit=limit), 'before': '{before}'.format(before=before)})
    posts = [0] * limit
    for post in res.json()['data']['children']:
        posts.append(post)
    return posts


def get_subreddits(limit=25, before=None):
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

    # here we pass our login method (password), username, and password
    data = {'grant_type': 'password',
            'username': REDDIT_USERNAME,
            'password': REDDIT_PASSWORD}

    # setup our header info, which gives reddit_api a brief description of our app
    headers = {'User-Agent': 'ReDatAPI v0.0.1'}

    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    # convert response to JSON and pull access_token value
    token = res.json()['access_token']

    # add authorization to our headers dictionary
    headers['Authorization'] = f"bearer {token}"

    # while the token is valid (~2 hours) we just add headers=headers to our requests
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    res = requests.get('https://oauth.reddit.com/hot', headers=headers,
                       params={'limit': '{limit}'.format(limit=limit), 'before': '{before}'.format(before=before)})

    data_frame = pandas.DataFrame()
    posts = [] * limit

    for post in res.json()['data']['children']:
        posts.append(post)
    return posts
