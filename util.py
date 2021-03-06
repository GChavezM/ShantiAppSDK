"""Internal utilities common to all modules"""
from datetime import datetime
import time
import json
import base64
import requests
import unicodedata

TOKEN = ''


def check_in_string(strings, original_string):
    """
    Function for checking if a string exists on a string.

    Args:
        strings (str): Strings to search.
        original_string (str): String to search in.

    Return:
        True if the strings exists in the original_string, False otherwise.
    """
    if strings and original_string:
        strings = strings.split()
        result = True
        for string in strings:
            if original_string.lower().find(string.lower()) < 0:
                result = False
        return result
    return True


def convert_date(hour, minute, year=0, month=0, day=0, simple_mode=False):
    """
    Function for converting python date into JavaScript date.

    Args:
        hour (int): Hour of date.
        minute (int): Minute of date.
        year (int): Year of date.
        month (int): Month of date.
        day (int): Day of date.
        simple_mode (bool): If True, simple mode is used without year, month and day variables.

    Return:
        Converted date.
    """
    if simple_mode:
        today = datetime.now()
        date = datetime(today.year, today.month, today.day, hour, minute)
    else:
        if year == 0 or month == 0 or day == 0:
            raise ValueError("Incorrect values")
        date = datetime(year, month, day, hour, minute)
    date_js = int(time.mktime(date.timetuple())) * 1000
    # offset = 2678400000
    # return date_js + offset
    return date_js


def fetch_cloud_functions(url, data, fetch_type='post'):
    """
    Function for fetching Firebase cloud functions.

    Args:
        url (str): Url of the Firebase cloud function.
        data (object): Data to send.
        fetch_type (str): Fetching options (optional).

    Return:
        Firebase cloud function response.
    """
    if TOKEN == '':
        raise ValueError('Import Token to module')
    response = requests.post(url=url, json=data,
                             headers={'Authorization': 'Bearer ' + TOKEN})
    if not response.ok:
        handle_request_error(response.text)
    print('Success')
    if fetch_type == 'get':
        return response.json()
    return True


def handle_request_error(response):
    """
    Handle error response from request.

    Args:
        response: Response from request.

    Raises:
        Error
    """
    error = json.loads(response)
    raise ValueError('Error:', error.get('error').get('message'))


def _get_image_base64(image):
    """
    Transform image to base64 format.

    Args:
        image: Image file.

    Returns:
        Image converted.
    """
    with open(image, "rb") as img_file:
        image_str = base64.b64encode(img_file.read())
    return image_str.decode('utf-8')


def upload_image(image, location, past_location=None):
    """
    Upload an image to Firebase storage.

    Args:
        image: Image file to upload.
        location (str): Destination in Firebase storage.
        past_location (str): Older image destination to delete

    Returns:
        dict: The image path and image uri.
    """
    if not image:
        return None
    url = 'https://us-central1-shantiapp-4eae1.cloudfunctions.net/uploadImage'
    image_data = {
        'base64': _get_image_base64(image),
        'imagePath': past_location
    }
    data = {
        'image': image_data,
        'location': location
    }
    return fetch_cloud_functions(url, data, fetch_type='get')


def strip_accents(text):
    """
    Remove string accents.

    Args:
        text: String to format.

    Returns:
        str: String formatted.
    """
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
    return str(text)


def make_email_address(name, last_name):
    """
    Create an email address string with a name and last name.

    Args:
        name: Name.
        last_name: Last name.

    Returns:
        str: Email address string.
    """
    name = name.replace(" ", "").lower()
    last_name = last_name.replace(" ", "").lower()
    name = strip_accents(name)
    last_name = strip_accents(last_name)
    return name + '.' + last_name + '@shanti.com'
