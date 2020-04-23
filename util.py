from datetime import datetime
import time
import json
import base64
import requests
from auth import get_token

api_key = None
MIN_DATA = {
    'office': ["name", "address"],
    'user': ["email", "password", "name"],
    'program': ["name", "type", "office", "teacher", "packages", "dates"]
}


def check_in_string(strings, original_string):
    if strings and original_string:
        strings = strings.split()
        result = True
        for string in strings:
            if original_string.lower().find(string.lower()) < 0:
                result = False
        return result
    return True


def convert_date(year, month, day, hour, minute):
    if year == 0 or month == 0 or day == 0:
        today = datetime.now()
        date = datetime(today.year, today.month - 1, today.day, hour, minute)
    else:
        date = datetime(year, month, day, hour, minute)
    date_js = int(time.mktime(date.timetuple())) * 1000
    offset = 2678400000
    return date_js + offset


def fetch_cloud_functions(token, url, data, fetch_type='post'):
    response = requests.post(url=url, json=data, headers={'Authorization': 'Bearer ' + token})
    if not response.ok:
        error = json.loads(response.text)
        print('Error', error.get('error').get('message'))
        return None
    print('Success')
    if fetch_type == 'get':
        return response.json()
    return True


def validate_data(data, data_type):
    min_data = MIN_DATA[data_type]
    if all(key in data for key in min_data):
        return True
    print('Insufficient Data')
    return False


def get_image_base64(image):
    with open(image, "rb") as img_file:
        image_str = base64.b64encode(img_file.read())
    return image_str.decode('utf-8')


def upload_image(image, location):
    if not image:
        return None
    token = get_token(api_key)
    url = 'https://us-central1-shantiapp-4eae1.cloudfunctions.net/uploadImage'
    data = {
        'image': get_image_base64(image),
        'location': location
    }
    return fetch_cloud_functions(token, url, data, fetch_type='get')
