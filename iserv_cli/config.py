import os
import json
import jwt
import time
from dotenv import load_dotenv
load_dotenv()

config_path = os.environ['ISERV_CONFIG_PATH']


class CliConfig:
    def __init__(self):
        self.values = self.load_config()

    def load_config(self):
        with open(f'{config_path}/iserv.json', 'r') as file:
            config = json.loads(file.read())
        return config

    def save_config(self):
        with open(f'{config_path}/iserv.json', 'w') as file:
            file.write(json.dumps(self.values))

    def get_token(self):
        token = self.values.get('token')

        if token is not None:
            payload = jwt.decode(
                token, options={"verify_signature": False})

            expiration = int(payload.get('exp'))
            if expiration > time.time():
                return token

    def save_token(self, token):
        self.values['token'] = token
        self.save_config()
