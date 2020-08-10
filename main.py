import requests
import json
import os
from urllib.parse import urlencode
from datetime import *
from tqdm import tqdm

# OAUTH_URL = 'https://oauth.vk.com/authorize'
# APP_ID = 7536762

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

ID = input('Введите ID пользователя VK: ')
YA_TOKEN = input('Введите токен с полигона Яндекс.Диска: ')
question = 0
while question != 'y' and question != 'n':
    question = input('Вы хотите изменить количество загружаемых фотографий (по умолчанию - 5)? (y/n): ')
if question == 'y':
    photo_count = int(input('Введите количество загружаемых фотографий: '))
else:
    photo_count = 5

VK_TOKEN = '510d2f3bd935bc86e8df8caf31c9b72b4609f6f327df7cb62ece43d3115f8e1ccc3893551a36b2f4b83b0'
response = requests.get(
    'https://api.vk.com/method/photos.get',
    params={
        'owner_id': ID,
        'album_id': 'profile',
        'extended': 1,
        'access_token': VK_TOKEN,
        'v': 5.21,
        'rev': 0,
        'photo_sizes': 1
    }
)

types_list = ['w', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's']

photos = []

for item in tqdm(response.json()['response']['items'], desc='Data retrieving'):
    not_found = True
    type_num = 0
    while not_found:
        size = 0
        while size < len(item['sizes']):
            if item['sizes'][size]['type'] != types_list[type_num]:
                size += 1
            else:
                tmp_date = f'_{datetime.date(datetime.fromtimestamp(item["date"]))}'
                photos.append({
                    'size': types_list[type_num],
                    'link': item['sizes'][size]['src'],
                    'height': item['sizes'][size]['height'],
                    'width': item['sizes'][size]['width'],
                    'date': tmp_date,
                    'likes': item['likes']['count']
                })
                not_found = False
                break
        type_num += 1

if len(photos) < photo_count:
    iter_count = len(photos)
else:
    iter_count = photo_count

json_data = []
count = 0
type_num = 0
while count < iter_count:   #test
    photo = 0
    while photo < len(photos):
        if photos[photo]['size'] != types_list[type_num]:
            photo += 1
        else:
            count += 1
            json_data.append(photos[photo])
            del photos[photo]
            if count > iter_count - 1:
                break
    type_num += 1

likes_count_tmp = {}

for photo in json_data:
    if photo['likes'] in likes_count_tmp:
        likes_count_tmp[photo['likes']] += 1
    else:
        likes_count_tmp.setdefault(photo['likes'], 1)

path = os.path.join(os.path.abspath(os.curdir), 'tmp_photos')
os.mkdir(path)

json_upl = []
for photo in tqdm(json_data, desc="Photo downloading from VK"):
    if likes_count_tmp[photo['likes']] > 1:
        photo['file_name'] = f'{photo["likes"]}{photo["date"]}.jpg'
    else:
        photo['file_name'] = f'{photo["likes"]}.jpg'
    dnld = requests.get(photo['link'])
    f_path = f'tmp_photos/{photo["file_name"]}'
    with open(f_path, 'wb') as f:
        f.write(dnld.content)
    json_upl.append({'file_name': photo['file_name'], 'size': photo['size']})

likes_count_tmp.clear()

params = {'path': 'photos_from_vk'}
headers = {'Authorization': f'OAuth {YA_TOKEN}'}
ya_resp = requests.put('https://cloud-api.yandex.net:443/v1/disk/resources', params=params, headers=headers)

with open('data.json', 'w') as f:
    json.dump(json_upl, f, indent=4)

for file in tqdm(os.listdir(path), desc='Photo uploading to Yandex.Disc'):
    file_name = file

    params = {'path': f'/photos_from_vk/{file_name}', 'overwrite': 'true'}
    upl_url = 'https://cloud-api.yandex.net:443/v1/disk/resources/upload'

    ya_resp = requests.get(upl_url, params=params, headers=headers)
    put_url = ya_resp.json().get('href')

    files = {'file': open(os.path.join(path, file_name), 'rb')}
    ya_resp = requests.put(put_url, files=files)
