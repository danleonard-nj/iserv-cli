from iserv_cli.config import CliConfig
from dotenv import load_dotenv
import requests
import os
load_dotenv()

client_id = os.environ['ISERV_CLIENT_ID']
client_secret = os.environ['ISERV_CLIENT_SECRET']
auth_url = os.environ['ISERV_AUTH_URL']


class CliAuth:
    def __init__(self):
        self.config = CliConfig()

    def get_token(self):
        cache_token = self.config.get_token()

        if cache_token is None:
            server_token = self.get_identity_server_token()
            self.config.save_token(server_token)

            return server_token
        else:
            return cache_token

    def get_identity_server_token(self):
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials',
            'scope': 'identity-server-admin'
        }

        response = requests.post(auth_url, data=data)
        return response.json().get('access_token')
