import json
import requests


def get_token(api_key, email="admin@shanti.com", password="shanti123"):
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + api_key
    data = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }
    response = requests.post(
        url=url,
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    if not response.ok:
        error = json.loads(response.text)
        print('Error', error.get('error').get('message'))
        return None
    result = response.json()
    id_token = result.get('idToken')
    return id_token
