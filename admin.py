"""Admin utilities"""
import requests
from _util import handle_request_error


class Admin:
    def __init__(self, api_key, email="admin@shanti.com", password="shanti123"):
        self._email = email
        self._password = password
        self._api_key = api_key
        self._token = self._get_token(email, password)

    @property
    def api_key(self):
        return self._api_key

    @property
    def token(self):
        return self._token

    def _get_token(self, email, password):
        url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + self.api_key
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
            handle_request_error(response.text)
        result = response.json()
        id_token = result.get('idToken')
        return id_token

    def update_token(self):
        self._token = self._get_token(self._email, self._password)
