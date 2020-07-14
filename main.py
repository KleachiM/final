import requests
import json
from urllib.parse import urlencode

from pprint import pprint

OAUTH_URL = 'https://oauth.vk.com/authorize'
APP_ID = 7536762

# OAUTH_DATA = {
#     'client_id': APP_ID,
#     'display': 'mobile',
#     'scope': 'photos, offline',
#     'response_type': 'token',
#     'v': 5.120,
# }
#
# print('?'.join(
#     (OAUTH_URL, urlencode(OAUTH_DATA))
# ))


token = '510d2f3bd935bc86e8df8caf31c9b72b4609f6f327df7cb62ece43d3115f8e1ccc3893551a36b2f4b83b0'

response = requests.get(
    'https://api.vk.com/method/photos.get',
    params={
        'owner_id': 4609665,
        'album_id': 'profile',
        'extended': 1,
        'access_token': token,
        'v': 5.21,
        'rev': 0,
        'photo_sizes': 1
    }
)

# print(response)
pprint(response.json())
# pprint(response.json()['response']['items'][-1]['sizes'][-1]['src'])

# dnld = requests.get(response.json()['response']['items'][-1]['sizes'][-1]['src'])
# with open('photo.jpg', 'wb') as f:
#     f.write(dnld.content)
