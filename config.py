"""Private Config File"""
import firebase_admin
from firebase_admin import credentials

SERVICE_ACCOUNT = 'service_account.json'  # Name of your json file

CREDENTIAL = credentials.Certificate(SERVICE_ACCOUNT)


def initialize_app():
    """
    Firebase Setup, initializes and returns a new App instance.

    Returns:
         Firebase App Instance
    """
    default_app = firebase_admin.initialize_app(
        credential=CREDENTIAL,
        options={
            'apiKey': "api_key",
            'authDomain': "auth_domain",
            'databaseURL': "database_url",
            'projectId': "project_id",
            'storageBucket': "storage_bucket",
            'messagingSenderId': "messaging_sender_id",
            'appId': "app_id",
            'measurementId': "measurement_id"
        }
    )
    return default_app


def remove_app(app):
    """
    Delete the specified Firebase App Instance

    Args:
        app: The App instance to be deleted
    """
    firebase_admin.delete_app(app)
