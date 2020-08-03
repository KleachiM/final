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

print(response)
types_list = ['w', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's']

# dnld = requests.get(response.json()['response']['items'][-1]['sizes'][-1]['src'])
# with open('photo.jpg', 'wb') as f:
#     f.write(dnld.content)

json_data = []

for item in response.json()['response']['items']:
    not_found = True
    type_num = 0
    while not_found:
        size = 0
        while size < len(item['sizes']):
            if item['sizes'][size]['type'] != types_list[type_num]:
                size += 1
            else:
                file_name = f'{item["likes"]["count"]}_{item["date"]}.jpg'
                json_data.append({'file_name': file_name, 'size': types_list[type_num]})
                not_found = False
                break
        type_num += 1

pprint(json_data)

# with open('data.json', 'a') as f:
        # json.dump(json_data, f)
