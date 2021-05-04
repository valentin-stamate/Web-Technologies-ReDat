import requests

CLIENT_ID = 'B1hmLU6wbT6SdQ'
SECRET_KEY = 'lZh7FRhuCZSTkPOIqHIvp-fkrHqKew'

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

with open('pw.txt', 'r') as f:
    passwd = f.read()
# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': '-lorenzo112-',
        'password': passwd}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'ReDatAPI v0.0.1'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

print(res)
print(res.json())
# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers['Authorization'] = f"bearer {TOKEN}"

# while the token is valid (~2 hours) we just add headers=headers to our requests
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

res = requests.get('https://oauth.reddit.com/r/games/hot', headers=headers)

for post in res.json()['data']['children']:
    print(post['data']['title'])
