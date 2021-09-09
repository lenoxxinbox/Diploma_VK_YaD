import requests
from pprint import pprint
import json
from datetime import datetime

# ###############################
# Читаем токен от API VK из файла
# ###############################

with open('token_test.txt', 'r') as file:
    token = file.read().strip()

# ########################################################
# Достаем фотографии с профиля, именуем количеством лайков
# ########################################################


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def take_photos(self, sorting=0):
        photos_url = self.url + 'photos.get'
        photos_params = {
            'owner_id': input('Введите id пользователя vk: '),
            'album_id': 'profile',
            'sort': sorting,
            'count': input('Введите необходимое количество фото: '),
            'photo_sizes': 1,
            'extended': 1
        }
        req = requests.get(photos_url, params={**self.params, **photos_params}).json()

        return req['response']['items']


vk_client = VkUser(token, '5.52')
photo_list = vk_client.take_photos()
# pprint(photo_list)

record = f'{datetime.now()} Take a photo from any users Vk account\n'
with open('log.txt', 'a') as log:
    log.write(record)
naming_list = []

for photo_unit in photo_list:

    name_photo = str(photo_unit['likes']['count']) + '.jpg'
    naming_list.append(name_photo)
    size = photo_unit['sizes']
    pprint(f"{name_photo} was saved")

    for unit in size:

        height_photo = unit['height']
        url_photo = unit['src']
        with open(name_photo, 'wb') as ph:
            response = requests.get(url_photo)
            ph.write(response.content)
# print(naming_list)

record = f'{datetime.now()} Collecting files to publish to the list\n'
with open('log.txt', 'a') as log:
    log.write(record)

# #################################
# Сохраняем фото в папке на Я.Диске
# #################################


class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        data = response.json()

        with open('data.json', 'a') as filej:
            json.dump(data, filej)

        return response.json()

    def upload_file_to_disk(self, disk_file_path, filename):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print(f"{filename} download successful")
            record = f'{datetime.now()} The file is saved on the Yandex. Disk\n'
            with open('log.txt', 'a') as log:
                log.write(record)


TOKEN = input('Введите токен с Полигона Яндекс.Диска: ')

if __name__ == '__main__':
    ya = YandexDisk(token=TOKEN)
    for name_unit in naming_list:
        ya.upload_file_to_disk(name_unit, name_unit)
