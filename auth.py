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
    if response.ok:
        result = response.json()
        idToken = result.get('idToken')
        return idToken
    else:
        print('Error', response.text)
        return
